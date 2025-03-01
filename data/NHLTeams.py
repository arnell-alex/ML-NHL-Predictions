# Dictionary of NHL teams with their base ESPN.com identifiers and abbreviations, keyed by full team name

NHL_TEAMS = {
    "Anaheim Ducks": {"abbr": "ana", "endpoint": "_/name/ana/anaheim-ducks"},
    "Boston Bruins": {"abbr": "bos", "endpoint": "_/name/bos/boston-bruins"},
    "Buffalo Sabres": {"abbr": "buf", "endpoint": "_/name/buf/buffalo-sabres"},
    "Calgary Flames": {"abbr": "cgy", "endpoint": "_/name/cgy/calgary-flames"},
    "Carolina Hurricanes": {"abbr": "car", "endpoint": "_/name/car/carolina-hurricanes"},
    "Chicago Blackhawks": {"abbr": "chi", "endpoint": "_/name/chi/chicago-blackhawks"},
    "Colorado Avalanche": {"abbr": "col", "endpoint": "_/name/col/colorado-avalanche"},
    "Columbus Blue Jackets": {"abbr": "cbj", "endpoint": "_/name/cbj/columbus-blue-jackets"},
    "Dallas Stars": {"abbr": "dal", "endpoint": "_/name/dal/dallas-stars"},
    "Detroit Red Wings": {"abbr": "det", "endpoint": "_/name/det/detroit-red-wings"},
    "Edmonton Oilers": {"abbr": "edm", "endpoint": "_/name/edm/edmonton-oilers"},
    "Florida Panthers": {"abbr": "fla", "endpoint": "_/name/fla/florida-panthers"},
    "Los Angeles Kings": {"abbr": "la", "endpoint": "_/name/la/los-angeles-kings"},
    "Minnesota Wild": {"abbr": "min", "endpoint": "_/name/min/minnesota-wild"},
    "Montreal Canadiens": {"abbr": "mtl", "endpoint": "_/name/mtl/montreal-canadiens"},
    "Nashville Predators": {"abbr": "nsh", "endpoint": "_/name/nsh/nashville-predators"},
    "New Jersey Devils": {"abbr": "nj", "endpoint": "_/name/nj/new-jersey-devils"},
    "New York Islanders": {"abbr": "nyi", "endpoint": "_/name/nyi/new-york-islanders"},
    "New York Rangers": {"abbr": "nyr", "endpoint": "_/name/nyr/new-york-rangers"},
    "Ottawa Senators": {"abbr": "ott", "endpoint": "_/name/ott/ottawa-senators"},
    "Philadelphia Flyers": {"abbr": "phi", "endpoint": "_/name/phi/philadelphia-flyers"},
    "Pittsburgh Penguins": {"abbr": "pit", "endpoint": "_/name/pit/pittsburgh-penguins"},
    "San Jose Sharks": {"abbr": "sj", "endpoint": "_/name/sj/san-jose-sharks"},
    "Seattle Kraken": {"abbr": "sea", "endpoint": "_/name/sea/seattle-kraken"},
    "St. Louis Blues": {"abbr": "stl", "endpoint": "_/name/stl/st-louis-blues"},
    "Tampa Bay Lightning": {"abbr": "tb", "endpoint": "_/name/tb/tampa-bay-lightning"},
    "Toronto Maple Leafs": {"abbr": "tor", "endpoint": "_/name/tor/toronto-maple-leafs"},
    "Utah Hockey Club": {"abbr": "utah", "endpoint": "_/name/utah/utah-hockey-club"},
    "Vancouver Canucks": {"abbr": "van", "endpoint": "_/name/van/vancouver-canucks"},
    "Vegas Golden Knights": {"abbr": "vgk", "endpoint": "_/name/vgk/vegas-golden-knights"},
    "Washington Capitals": {"abbr": "wsh", "endpoint": "_/name/wsh/washington-capitals"},
    "Winnipeg Jets": {"abbr": "wpg", "endpoint": "_/name/wpg/winnipeg-jets"}
}

def getTeamEndpoint(team_name, subpath=""):
    team = NHL_TEAMS.get(team_name)
    if not team:
        return None
    return f"team/{subpath}/{team['endpoint']}" if subpath else f"team{team['endpoint']}"

def getTeamAbbr(team_name):
    team = NHL_TEAMS.get(team_name)
    return team["abbr"] if team else None

if __name__ == "__main__":
    # Test the functions
    print(getTeamEndpoint("Boston Bruins"))              # team/_/name/bos/boston-bruins
    print(getTeamEndpoint("Boston Bruins", "roster"))    # team/roster/_/name/bos/boston-bruins
    print(getTeamEndpoint("Boston Bruins", "stats"))     # team/stats/_/name/bos/boston-bruins
    print(getTeamAbbr("Boston Bruins"))                  # bos
    print(getTeamEndpoint("Fake Team"))                  # None