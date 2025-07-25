def tables() -> tuple[str]:
    """helper function to get all tables' names within the database"""
    tables = set()
    with open("src/LibrarySchema.sql") as schema:
            for line in schema.readlines():
                spaced = line.split()
                if spaced != []:
                    if spaced[0] == "CREATE" and spaced[1] == "TABLE":
                        tables.add(spaced[2].rstrip("\n")[:len(spaced[2]) - 1])
    return tuple(tables)

TABLES = tables()

def columns_by_table() -> dict[str : tuple[str]]:
    """helper function which builds a dictionary of all the tables that is the key to a tuple of all column names"""
    ret = dict()
    with open("src/LibrarySchema.sql") as schema:
        li = list()
        tab = ""
        in_table = False
        for line in schema.readlines():
            if not in_table:
                spaced = line.split()
                if spaced != []:
                    if spaced[0] == "CREATE" and spaced[1] == "TABLE":
                        tab = spaced[2].rstrip("\n")[:len(spaced[2]) - 1]
                        in_table = True
            else:
                if line.startswith("\t"):
                    line = line.strip("\t")
                    spaced = line.split()
                    li.append(spaced[0])
                else:
                    in_table = False
                    ret[tab] = li.copy()
                    li.clear()
                    continue
    return ret
    
COLUMNS = columns_by_table()

def libraries() -> tuple[str]:
    with open("src/LibrarySchema.sql") as schema:
        tup = tuple()
        poi = None
        for line in schema.readlines():
            line = line.split()
            if len(line) > 3:
                if line[2] == "libs":
                    poi = line[4:]
                    break
        for i in range(len(poi)):
            val = poi[i]
            poi[i] = val.replace(',', "").replace("\'", "")
        poi[0] = poi[0].split("(")[1]
        poi[len(poi) - 1] = poi[len(poi) - 1].split(")")[0]
        tup = tuple(poi)
        return tup
    
LIBRARIES = libraries()