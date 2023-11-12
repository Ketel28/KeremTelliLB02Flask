from functools import reduce
from flask import Flask, jsonify

app = Flask(__name__)

class Player:
    def __init__(self, name, age, goals):
        self.name = name
        self.age = age
        self.goals = goals

    def to_dict(self):
        return {"name": self.name, "age": self.age, "goals": self.goals}

class PlayerStats:
    def __init__(self, player):
        self.player = player

    def get_stats(self):
        return {"Spieler": self.player.name, "Alter": self.player.age, "Tore": self.player.goals}

def apply_operations_to_players(players, map_func=None, reduce_func=None, filter_func=None):
    if map_func:
        players = list(map(map_func, players))
    if filter_func:
        players = list(filter(filter_func, players))
    if reduce_func:
        players = reduce(reduce_func, players)

    return players

# Kommentar für möglichen Test der apply_operations_to_players-Funktion
# Hier könnte man testen, ob die Funktion korrekt mappt, filtert und reduziert.

def update_player_age(players, player_name, new_age):
    updated_players = players.copy()
    for player in updated_players:
        if player.name == player_name:
            player.age = new_age
    return updated_players

def serialize_player(player):
    return player.to_dict()

def calculate_total_goals(players):
    total_goals = reduce(lambda acc, player: acc + player.goals, players, 0)
    return total_goals

def transform_to_dict(players):
    player_dict = reduce(lambda acc, player: {**acc, player.name: {"Alter": player.age, "Tore": player.goals}}, players, {})
    return player_dict

# Kommentar für möglichen Test der /player_dict-Route
# Hier könnte man testen, ob die Spielerdaten korrekt in ein Dictionary transformiert werden.

# Erstelle eine Liste aller Spieler
players = [
    Player(name="Messi", age=34, goals=45),
    Player(name="Neymar", age=29, goals=20),
    Player(name="Suarez", age=34, goals=30),
    Player(name="Pique", age=37, goals=5)
]

def get_player_stats(player):
    return {"Spieler": player.name, "Alter": player.age, "Tore": player.goals}

def show_stats(players):
    map_func = get_player_stats
    sorted_stats = apply_operations_to_players(players, map_func, None, None)
    sort_func = lambda stat: stat["Tore"]
    sorted_stats = sorted(sorted_stats, key=sort_func, reverse=True)
    return jsonify(player_stats=sorted_stats)

def top_scorer(players):
    filter_func = lambda player: player.goals > 20
    top_scorers = apply_operations_to_players(players, None, None, filter_func)
    top_scorer_names = [player.name for player in top_scorers]
    return f"Top Torschützen: {', '.join(top_scorer_names)}"

@app.route('/player_dict')
def get_player_dict():
    global players
    transformed_data = transform_to_dict(players)
    return jsonify(players=transformed_data)

@app.route('/displayStats')
def display_stats():
    global players
    return show_stats(players)

@app.route('/total_goals')
def total_goals():
    global players
    total_goals_value = calculate_total_goals(players)
    return f"Gesamtanzahl der Tore: {total_goals_value}"

# Kommentar für möglichen Test der /total_goals-Route
# Hier könnte man testen, ob die Gesamtzahl der Tore korrekt berechnet wird.

@app.route('/')
def welcome():
    return f'Willkommen bei der Fussballanalyse'

@app.route('/players')
def get_players():
    global players
    map_func = lambda player: player.to_dict()
    return jsonify(players=apply_operations_to_players(players, map_func))

@app.route('/update_age')
def update_age():
    global players
    updated_players = update_player_age(players, "Messi", 35)
    serialized_players = list(map(serialize_player, updated_players))
    return jsonify(updated_players=serialized_players)

@app.route('/average_age')
def average_age():
    global players
    reduce_func = lambda acc, player: acc + player.age if isinstance(acc, int) else acc.age + player.age
    total_age = apply_operations_to_players(players, None, reduce_func)
    average_age_value = total_age / len(players)
    return f"Durchschnittsalter: {average_age_value:.2f}"

# Kommentar für möglichen Test der /average_age-Route
# Hier könnte man testen, ob das Durchschnittsalter korrekt berechnet wird.

@app.route('/top_scorer')
def get_top_scorer():
    global players
    return top_scorer(players)

if __name__ == '__main__':
    app.run(debug=True)