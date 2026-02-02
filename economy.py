“””
Economy management for Starlightdeck V2
Handles Careon currency transactions and tracking
“””

import json
from pathlib import Path

class Economy:
def **init**(self, bank_file=“careon_bank_v2.json”):
self.bank_file = bank_file
self.load_bank()

```
def load_bank(self):
    """Load bank data from JSON file"""
    try:
        with open(self.bank_file, 'r') as f:
            self.bank_data = json.load(f)
    except FileNotFoundError:
        self.bank_data = {}

def save_bank(self):
    """Save bank data to JSON file"""
    with open(self.bank_file, 'w') as f:
        json.dump(self.bank_data, f, indent=2)

def get_balance(self, user_id):
    """Get user's Careon balance"""
    return self.bank_data.get(user_id, {}).get('balance', 0)

def add_careon(self, user_id, amount):
    """Add Careon to user account"""
    if user_id not in self.bank_data:
        self.bank_data[user_id] = {'balance': 0}
    self.bank_data[user_id]['balance'] += amount
    self.save_bank()
    return self.bank_data[user_id]['balance']

def deduct_careon(self, user_id, amount):
    """Deduct Careon from user account"""
    if user_id not in self.bank_data:
        return False
    if self.bank_data[user_id]['balance'] >= amount:
        self.bank_data[user_id]['balance'] -= amount
        self.save_bank()
        return True
    return False

def transfer_careon(self, from_user, to_user, amount):
    """Transfer Careon between users"""
    if self.deduct_careon(from_user, amount):
        self.add_careon(to_user, amount)
        return True
    return False
```

# Community fund management

class CommunityFund:
def **init**(self):
self.fund_balance = 0

```
def add_to_fund(self, amount):
    """Add to community fund"""
    self.fund_balance += amount
    return self.fund_balance

def get_fund_balance(self):
    """Get current community fund balance"""
    return self.fund_balance
```