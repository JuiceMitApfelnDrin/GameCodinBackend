from dataclasses import dataclass


class User:
  def __init__(self, username, email):
    self.username = username
    self.email = email