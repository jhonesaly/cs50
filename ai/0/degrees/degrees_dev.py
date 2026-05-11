import csv
import sys

from util import Node, StackFrontier, QueueFrontier
from pprint import pprint

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # config
    start = Node(state=source, parent=None, action=None)
    goal = Node(state=target, parent=None, action=None)
    frontier = QueueFrontier()
    explored = set()
    response = []

    frontier.add(start)
    i = 0

    # loop
    while True:
        i += 1
        print(f"\n---iteration {i}---")

        # situation report at beginning of iteration
        print(f"initial frontier:")
        for node in frontier.frontier:
            print(f"{person_name(node.state)}")
        
        print(f"explored:")
        for node in explored:
            print(f"{person_name(node.state)}")

        # there are no more nodes to explore
        if frontier.empty():
            return None
        
        node = frontier.remove() # selection of node

        # selected node report
        print(f"selected node: {person_name(node.state)}")
        print(f"goal node: {person_name(goal.state)}")

        # selected node is the goal
        if node.state == goal.state:
            print("\n---Found a solution!---")
            # backtrack to construct the path
            while node.parent is not None:
                response.append((node.action, node.state))
                node = node.parent
            break

        # selected node is not the goal
        if node.state != goal.state:
            explored.add(node) # mark node as explored
            
            # add neighbors to node
            for action, state in neighbors_for_person(node.state):
                # only add neighbor if it is not already in frontier or explored
                if not frontier.contains_state(state) and not any(n.state == state for n in explored):
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    # reverse the path to get it from source to target
    return response[::-1]


def parse_args():
    """
    Parse command line arguments in the format: key=value
    Returns a dictionary with the parsed arguments.
    """
    kwargs = {}
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            kwargs[key] = value
    return kwargs


def main():
    print(f"argumentos sys.argv: {sys.argv}")
    
    # Parse arguments
    kwargs = parse_args()
    directory = kwargs.get('directory', 'small')
    source_input = kwargs.get('source', "Tom Cruise")
    target_input = kwargs.get('target', "Tom Hanks")

    # Load data from files into memory
    print(f"Loading data from {directory}...")
    load_data(directory)
    print("Data loaded.")

    # Get source name (from argument or input)
    if source_input is None:
        source = person_id_for_name(input("Name: "))
    else:
        source = person_id_for_name(source_input)
    print(f"source name: {source_input}, id: {source}")

    if source is None:
        sys.exit("Person not found.")
    
    # Get target name (from argument or input)
    if target_input is None:
        target = person_id_for_name(input("Name: "))
    else:
        target = person_id_for_name(target_input)
    print(f"target name: {target_input}, id: {target}")

    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)
    print(f"path: {path}")

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]

  
def person_name(id):
    """
    Returns the name of the person for a given id.
    """
    return people[id]["name"]


def movie_title(id):
    """
    Returns the name of the movie for a given id.
    """
    return movies[id]["title"]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
