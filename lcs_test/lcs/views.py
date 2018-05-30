# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

import json

# Create your views here.
@csrf_exempt
def find_lcs(request):
  data = {
    "status": "Error",
    "message": "",
  }

  if request.method != 'POST':
    data['message'] = 'A POST request with json payload is expected.'
    return HttpResponseBadRequest(json.dumps(data), 'application/json')

  the_set = {}
  try:
    strings = json.loads(request.body)
    if 'setOfStrings' not in strings:
      raise ValueError()
    if not strings['setOfStrings']:
      raise ValueError('setOfStrings should not be empty')
    for item in strings['setOfStrings']:
      if 'value' not in item:
        raise ValueError()
      if item['value'] in the_set:
        raise ValueError('setOfStrings should be a set, all of its values should be unique')
      else:
        the_set[item['value']] = 1
  except ValueError as e:
    data['message'] = """Payload of the request should be in the following form
        { "setOfStrings": [ {"value": "string1"}, {"value": "string2"} ..] }"""
    if e.message:
      data['message'] = e.message
    return HttpResponseBadRequest(json.dumps(data), 'application/json')

  values = the_set.keys()
  shortest = min(values, key=len)
  all_lcs = []
  current = ""
  for ch in shortest:
    current += ch
    if inSet(current, values):
      if current[:-1] in all_lcs:
        all_lcs.remove(current[:-1])
      all_lcs.append(current)
    else:
      while current:
        current = current[1:]
        if inSet(current, values):
          break

  data['status'] = 'OK'
  if all_lcs:
    s = sorted(all_lcs, key=len, reverse=True)
    data['lcs'] = [{"value": s[0]}]
  else:
    data['message'] = 'No common string was found'
    data['lcs'] = []
  return HttpResponse(json.dumps(data), 'application/json')


def inSet(string, l):
  for item in l:
    if string not in item:
      return False
  return True
