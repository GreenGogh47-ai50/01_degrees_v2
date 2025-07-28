import csv
import sys
import pdb

from util import Node, StackFrontier, QueueFrontier

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


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # source = person_id_for_name(input("Name: "))
    # if source is None:
    #     sys.exit("Person not found.")
    # target = person_id_for_name(input("Name: "))
    # if target is None:
    #     sys.exit("Person not found.")

    source = person_id_for_name("Sally Field") #ID 398
    target = person_id_for_name("Valeria Golino") #ID 420

    path = shortest_path(source, target)

    # Must output as ([movie, name], [movie, name], [movie, name])

    if path is None:
        print("Not connected.")
    else:
        pdb.set_trace()
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    INSTRUCTIONS
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.

    # ===========================================
    PSUDOCODE

    I need:
        - [x] frontier for the UNexplored neighbors
        - [x] Empty set for the EXPLORED nodes
        - [x] initial state (first actor node)
        - [ ] track actions and transitions
        - [ ] goal test
        - [ ] path cost function
    """
    first_actor = Node(state=source, parent=None, action=None)
    goal_actor = target
    frontier = QueueFrontier()
    explored = set()
    frontier.add(first_actor)

    print(f"First Actor: #{first_actor.state}, #{first_actor.parent}, #{first_actor.action}")

    # Add the first actor to the list of UNEXPLORED nodes

    while frontier.empty() == False:
        node = frontier.remove()
        explored.add(node.state)

        # Get the neighboring actors, iterate through them

        for movie_id, person_id in neighbors_for_person(node.state):
            print(f"movie_id: #{movie_id}, person_id: #{person_id}")
            # Skip if explored
            if person_id in explored:
                continue
            # If it's not the goal, made a node
            if person_id != goal_actor: # Written this way, I'm not actually adding that last node.
                child = Node(state=person_id, parent=node, action=movie_id)
                frontier.add(child)
            else:
                path = [[movie_id, person_id]]
                pdb.set_trace()
                while node.parent != None:
                    path.append([node.action,node.state])
                    node = node.parent # Having this before the append was canceling my while statement.

                    # Insert and ruby unshift are different.
                    # That's why the instructor told us to reverse the value.
                pdb.set_trace()
                return path
                # I can't just call path.reverse because it creates a different object type.
                # Like when I was trying to call an index on a set.



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
