#!/usr/bin/env python3

import time
import requests
import json


class ApiException(Exception):
    pass


class ToornamentClient:
    """
    Main client class

    Methods:
        disciplines

        tournaments
        create_tournament
        get_tournament
        edit_tournament
        delete_tournament
        my_tournaments

        matches
        get_match
        edit_match
        get_match_result
        edit_match_result
        matches_by_discipline

        games
        get_game
        edit_game
        get_game_result
        edit_game_result

        participants
        create_participant
        get_participant
        edit_participant
        delete_participant

        schedules

        stages
        get_tournament_stage
        get_stage
    """

    def __init__(self, client_id, client_secret, api_key):
        """
        :param client_id
        :param client_secret
        :param api_key

        :return ToornamentClient object
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_key = api_key
        self.expire_date = 0
        self._request_new_token()

    def _make_request(self, method, url, body={}, headers={}):
        r = requests.request(method, url, json=body, headers=headers)

        try:
            res = json.loads(r.text)
        except json.decoder.JSONDecodeError:
            # Response doesn't have body (ex: delete_tournament())
            res = "Error code " + str(r.status_code)

        if not r.ok:
            raise ApiException(res)
        return res

    def _request_new_token(self):
        url = 'https://api.toornament.com/oauth/v2/token'
        body = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        r = self._make_request("post", url, body)

        now = int(time.time())
        self.expire_date = now + r['expires_in'] - 1  # 1 second to be sure it is not already expired
        self.access_token = r['access_token']
        self.token_type = r['token_type']
        self.headers = {
            'X-Api-Key': self.api_key,
            'Authorization': self.token_type.title() + ' ' + self.access_token
        }
        return r['access_token']

    def _update_token(self):
        # Update if token is expired
        now = int(time.time())
        if self.expire_date > now:
            return self.access_token
        return self._request_new_token()

    def disciplines(self, id=None):
        # https://developer.toornament.com/doc/disciplines

        self._update_token()  # Be sure token is still valid

        url = 'https://api.toornament.com/v1/disciplines'
        if id is not None:
            url += '/' + id

        return self._make_request("get", url, headers=self.headers)

    def tournaments(self, discipline=None, status=None, featured=None, online=None, country=None, after_start=None,
                    before_start=None, after_end=None, before_end=None, sort='date_desc', name=None):
        # https://developer.toornament.com/doc/tournaments

        self._update_token()  # Be sure token is still valid

        url = 'https://api.toornament.com/v1/tournaments'

        body = {
            'discipline': discipline,
            'status': status,
            'featured': featured,
            'online': online,
            'country': country,
            'after_start': after_start,
            'before_start': before_start,
            'after_end': after_end,
            'before_end': before_end,
            'sort': sort,
            'name': name
        }

        return self._make_request("get", url, body=body, headers=self.headers)

    def create_tournament(self, discipline, name, size, participant_type, full_name=None, organization=None,
                          website=None, date_start=None, date_end=None, timezone=None, online=None, public=None,
                          location=None, country=None, description=None, rules=None, prize=None, check_in=None, participant_nationality=None, match_format=None):
        # Authorized Access only!
        # https://developer.toornament.com/doc/tournaments

        self._update_token()  # Be sure token is still valid

        url = 'https://api.toornament.com/v1/tournaments'

        body = {
            'discipline': discipline,
            'name': name,
            'size': size,
            'participant_type': participant_type,
            'full_name': full_name,
            'organization': organization,
            'website': website,
            'date_start': date_start,
            'date_end': date_end,
            'timezone': timezone,
            'online': online,
            'public': public,
            'location': location,
            'country': country,
            'description': description,
            'rules': rules,
            'prize': prize,
            'check_in': check_in,
            'participant_nationality': participant_nationality,
            'match_format': match_format
        }

        return self._make_request("post", url, body=body, headers=self.headers)

    def get_tournament(self, id, with_streams=0):
        # https://developer.toornament.com/doc/tournaments

        self._update_token()  # Be sure token is still valid

        url = 'https://api.toornament.com/v1/tournaments/' + id

        body = {
            'with_streams': with_streams
        }

        return self._make_request("get", url, body=body, headers=self.headers)

    def edit_tournament(self, id, name, size, full_name, organization, website, date_start, date_end, timezone, online,
                        public, location, country, description, rules, prize, check_in, participant_nationality, match_format):
        # Authorized Access only!
        # https://developer.toornament.com/doc/tournaments

        self._update_token()  # Be sure token is still valid

        url = 'https://api.toornament.com/v1/tournaments/' + id

        body = {
            "name": name,
            "size": size,
            "full_name": full_name,
            "organization": organization,
            "website": website,
            "date_start": date_start,
            "date_end": date_end,
            "timezone": timezone,
            "online": online,
            "public": public,
            "location": location,
            'description': description,
            'rules': rules,
            'prize': prize,
            "country": country,
            "check_in": check_in,
            "participant_nationality": participant_nationality,
            "match_format": match_format
        }

        return self._make_request("patch", url, body=body, headers=self.headers)

    def delete_tournament(self, id):
        # Authorized Access only!
        # https://developer.toornament.com/doc/tournaments

        self._update_token()  # Be sure token is still valid

        url = 'https://api.toornament.com/v1/tournaments/' + id

        return self._make_request("delete", url, headers=self.headers)

    def my_tournaments(self, name=None, discipline=None, status=None, archived=None, online=None, country=None,
                       after_start=None, before_start=None, after_end=None, before_end=None, sort=None, page=None):
        # Authorized Access only!
        # https://developer.toornament.com/doc/tournaments

        self._update_token()  # Be sure token is still valid

        url = 'https://api.toornament.com/v1/me/tournaments'

        body = {
            'name': name,
            'discipline': discipline,
            'status': status,
            'archived': archived,
            'online': online,
            'country': country,
            'after_start': after_start,
            'before_start': before_start,
            'after_end': after_end,
            'before_end': before_end,
            'sort': sort,
            'page': page
        }

        return self._make_request("get", url, body=body, headers=self.headers)

    def matches(self, tournament_id, has_result=None, stage_number=None, group_number=None, round_number=None,
                sort=None, participant_id=None, with_games=None):
        # https://developer.toornament.com/doc/matches

        url = 'https://api.toornament.com/v1/tournaments/' + tournament_id + '/matches'

        body = {
            'has_result': has_result,
            'stage_number': stage_number,
            'group_number': group_number,
            'round_number': round_number,
            'sort': sort,
            'participant_id': participant_id,
            'with_games': with_games
        }

        return self._make_request("get", url, body=body, headers=self.headers)

    def get_match(self, tournament_id, id, with_games=None):
        # https://developer.toornament.com/doc/matches

        url = 'https://api.toornament.com/v1/tournaments/' + tournament_id + '/matches/' + id

        body = {
            'has_result': has_result,
            'stage_number': stage_number,
            'group_number': group_number,
            'round_number': round_number,
            'sort': sort,
            'participant_id': participant_id,
            'with_games': with_games
        }

        return self._make_request("get", url, body=body, headers=self.headers)

    def edit_match(self, tournament_id, id, date, timezone, match_format, note, private_note, streams=None, vods=None):
        # Authorized access only!
        # https://developer.toornament.com/doc/matches

        url = 'https://api.toornament.com/v1/tournaments/' + tournament_id + '/matches/' + id

        body = {
            'date': date,
            'timezone': timezone,
            'match_format': match_format,
            'note': note,
            'private_note': private_note,
            'streams': streams,
            'vods': vods
        }

        return self._make_request("patch", url, body=body, headers=self.headers)

    def get_match_result(self, tournament_id, id):
        # https://developer.toornament.com/doc/matches

        url = 'https://api.toornament.com/v1/tournaments/' + tournament_id + '/matches/' + id + '/result'

        return self._make_request("get", url, headers=self.headers)

    def edit_match_result(self, tournament_id, id, status, opponents):
        # Authorized access only!
        # https://developer.toornament.com/doc/matches

        url = 'https://api.toornament.com/v1/tournaments/' + tournament_id + '/matches/' + id + '/result'

        body = {
            'status': status,
            'opponents': opponents
        }

        return self._make_request("put", url, body=body, headers=self.headers)

    def matches_by_discipline(self, discipline_id, featured, has_result, sort, participant_id, tournament_ids,
                              with_games, before_date, after_date, page):

        # https://developer.toornament.com/doc/matches

        url = 'https://api.toornament.com/v1/disciplines/' + discipline_id + '/matches/'

        body = {
            'featured': featured,
            'has_result': has_result,
            'sort': sort,
            'participant_id': participant_id,
            'tournament_ids': tournament_ids,
            'with_games': with_games,
            'before_date': before_date,
            'after_date': after_date,
            'page': page
        }

        return self._make_request("get", url, body=body, headers=self.headers)

    def games(self, tournament_id, match_id, with_stats=None):
        # https://developer.toornament.com/doc/games

        url = 'https://api.toornament.com/v1/tournaments/' + tournament_id + '/matches/' + match_id + '/games'

        body = {
            'with_stats': with_stats
        }

        return self._make_request("get", url, body=body, headers=self.headers)

    def get_game(self, tournament_id, match_id, number, with_games=None):
        # https://developer.toornament.com/doc/games

        url = 'https://api.toornament.com/v1/tournaments/' + tournament_id + '/matches/' + match_id + '/games/' + number

        body = {
            'with_games': with_games
        }

        return self._make_request("get", url, body=body, headers=self.headers)

    # Work in progress:
    def edit_game(self, tournament_id, match_id, number, body={}):
        # Authorized access only!
        # README: Please go to https://developer.toornament.com/doc/games#patch:tournaments:tournament_id:matches:match_id:games:number,
        # select your discipline from top right corner, and see the body's structure for your specific discipline

        url = 'https://api.toornament.com/v1/tournaments/' + tournament_id + '/matches/' + match_id + '/games/' + number

        return self._make_request("patch", url, body=body, headers=self.headers)

    def get_game_result(self, tournament_id, match_id, number):
        # https://developer.toornament.com/doc/games

        url = 'https://api.toornament.com/v1/tournaments/' + tournament_id + '/matches/' + match_id + '/games/' + number + '/result'

        return self._make_request("patch", url, headers=self.headers)

    # Based on discipline:
    # TODO: Parameters
    def edit_game_result(self, tournament_id, match_id, number, status, opponents, update_match=None):
        # Authorized access only!
        # https://developer.toornament.com/doc/games

        url = 'https://api.toornament.com/v1/tournaments/' + tournament_id + '/matches/' + match_id + '/games/' + number + '/result'

        params = {
            'update_match': update_match
        }

        body = {
            'status': status,
            'opponents': opponents
        }

        return self._make_request("put", url, body=body, headers=self.headers)

    def participants(self, tournament_id, with_lineup=None, with_custom_fields=None, sort=None):
        # https://developer.toornament.com/doc/participants

        url = 'https://api.toornament.com/v1/tournaments/' + tournament_id + '/participants'

        body = {
            'with_lineup': with_lineup,
            'with_custom_fields': with_custom_fields,
            'sort': sort
        }

        return self._make_request("get", url, body=body, headers=self.headers)

    def create_participant(self, tournament_id, name, email=None, country=None, lineup=None):
        # Authorized Access only!
        # https://developer.toornament.com/doc/participants

        self._update_token()  # Be sure token is still valid

        url = 'https://api.toornament.com/v1/tournaments/' + tournament_id + '/participants'

        body = {
            'name': name,
            'email': email,
            'country': country,
            'lineup': lineup
        }
        return self._make_request("post", url, body=body, headers=self.headers)

    def get_participant(self, tournament_id, id):
        # https://developer.toornament.com/doc/participants

        url = 'https://api.toornament.com/v1/tournaments/' + tournament_id + '/participants/' + id

        return self._make_request("get", url, headers=self.headers)

    def edit_participant(self, tournament_id, id, name, email=None, country=None, lineup=None):
        # Authorized Access only!
        # https://developer.toornament.com/doc/participants

        self._update_token()  # Be sure token is still valid

        url = 'https://api.toornament.com/v1/tournaments/' + tournament_id + '/participants/' + id

        body = {
            'name': name,
            'email': email,
            'country': country,
            'lineup': lineup
        }

        return self._make_request("patch", url, body=body, headers=self.headers)

    def delete_participant(self, tournament_id, id):
        # Authorized Access only!
        # https://developer.toornament.com/doc/participants

        self._update_token()  # Be sure token is still valid

        url = 'https://api.toornament.com/v1/tournaments/' + tournament_id + '/participants/' + id

        return self._make_request("delete", url, headers=self.headers)

    def schedules(self, tournament_id, with_events=None, visibility=None):
        # https://developer.toornament.com/doc/schedules

        url = 'https://api.toornament.com/v1/tournaments/' + tournament_id + '/schedules'

        body = {
            'with_events': with_events,
            'visibility': visibility
        }

        return self._make_request("get", url, body=body, headers=self.headers)

    def stages(self, tournament_id):
        # https://developer.toornament.com/doc/stages

        url = 'https://api.toornament.com/v1/tournaments/' + tournament_id + '/stages'

        return self._make_request("get", url, headers=self.headers)

    def get_tournament_stage(self, tournament_id, number, with_groups=None, with_rounds=None):
        # https://developer.toornament.com/doc/stages

        url = 'https://api.toornament.com/v1/tournaments/' + tournament_id + '/schedules/' + number

        body = {
            'with_groups': with_groups,
            'with_rounds': with_rounds
        }

        return self._make_request("get", url, body=body, headers=self.headers)

    def get_stage(self, tournament_id, number, bracket_layout=None):
        # https://developer.toornament.com/doc/stages

        url = 'https://api.toornament.com/v1/tournaments/' + tournament_id + '/schedules/' + number + '/view'

        body = {
            'bracket_layout': bracket_layout
        }

        return self._make_request("get", url, body=body, headers=self.headers)