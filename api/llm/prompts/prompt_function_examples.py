PROMPT_FUNCTION_EXAMPLES = """
- id: 1
  function_type: "coordinates"
  task_type: "Move Towards Center"
  objective: "Agents move towards the center of the map."
  python_function: |
    def move_towards_center(N: int, Objects: list, BBox: list[int]) -> list[tuple[int, int]]:
        center_x = (BBox[0] + BBox[2]) / 2
        center_y = (BBox[1] + BBox[3]) / 2
        return [(center_x, center_y)] * N

- id: 2
  function_type: "coordinates"
  task_type: "Avoid Object"
  objective: "Agents avoid the largest object on the map by moving to the opposite side of the map."
  python_function: |
    def avoid_largest_object(N: int, Objects: list, BBox: list[int]) -> list[tuple[int, int]]:
        largest_object = max(Objects, key=lambda obj: obj["radius"])
        opposite_x = BBox[2] - largest_object["position"][0]
        opposite_y = BBox[3] - largest_object["position"][1]
        return [(opposite_x, opposite_y)] * N

- id: 3
  function_type: "coordinates"
  task_type: "Spread Out"
  objective: "Agents spread out evenly in a line along the x-axis within the bounding box."
  python_function: |
    def spread_out_in_line(N: int, Objects: list, BBox: list[int]) -> list[tuple[int, int]]:
        x_min, x_max = BBox[0], BBox[2]
        y_coord = (BBox[1] + BBox[3]) / 2  # Move along the center y-line
        step = (x_max - x_min) / (N - 1) if N > 1 else 0
        return [(x_min + i * step, y_coord) for i in range(N)]

- id: 4
  function_type: "coordinates"
  task_type: "Move Towards Closest Tree"
  objective: "Agents move towards the closest tree on the map."
  python_function: |
    def move_towards_tree(N: int, Objects: list, BBox: list[int]) -> list[tuple[int, int]]:
        trees = [obj for obj in Objects if obj["object_type"] == "Tree"]
        if not trees:
            # If there are no trees, stay in place
            return [(BBox[0], BBox[1])] * N
        # Find the closest tree (minimize distance from (0, 0) to the tree's position)
        closest_tree = min(trees, key=lambda tree: (tree["position"][0]**2 + tree["position"][1]**2))
        return [tuple(closest_tree["position"])] * N

- id: 5
  function_type: "coordinates"
  task_type: "Distribute Along Bounding Box Perimeter"
  objective: "Agents are distributed along the bounding box perimeter edges evenly."
  python_function: |
    def patrol_bbox_perimeter(N: int, Objects: list, BBox: list[int]) -> list[tuple[int, int]]:
        perimeter_length = 2 * ((BBox[2] - BBox[0]) + (BBox[3] - BBox[1]))
        step = perimeter_length / N
        coordinates = []
        for i in range(N):
            distance = step * i
            if distance <= (BBox[2] - BBox[0]):  # Top edge
                x = BBox[0] + distance
                y = BBox[1]
            elif distance <= (BBox[2] - BBox[0]) + (BBox[3] - BBox[1]):  # Right edge
                x = BBox[2]
                y = BBox[1] + (distance - (BBox[2] - BBox[0]))
            elif distance <= 2 * (BBox[2] - BBox[0]) + (BBox[3] - BBox[1]):  # Bottom edge
                x = BBox[2] - (distance - (BBox[2] - BBox[0]) - (BBox[3] - BBox[1]))
                y = BBox[3]
            else:  # Left edge
                x = BBox[0]
                y = BBox[3] - (distance - 2 * (BBox[2] - BBox[0]) - (BBox[3] - BBox[1]))
            coordinates.append((x, y))
        return coordinates

- id: 6
  function_type: "coordinates"
  task_type: "Guard Bounding Box Corners"
  objective: "Agents move to the four corners of the bounding box, dividing evenly between them."
  python_function: |
    def guard_bbox_corners(N: int, Objects: list, BBox: list[int]) -> list[tuple[int, int]]:
        corners = [(BBox[0], BBox[1]), (BBox[2], BBox[1]), (BBox[2], BBox[3]), (BBox[0], BBox[3])]
        return [corners[i % 4] for i in range(N)]

- id: 7
  function_type: "coordinates"
  task_type: "Even Distribution Along Bounding Box Perimeter"
  objective: "Agents distribute evenly along the bounding box perimeter, ensuring uniform spacing."
  python_function: |
    def even_distribution_bbox_perimeter(N: int, Objects: list, BBox: list[int]) -> list[tuple[int, int]]:
        perimeter_length = 2 * ((BBox[2] - BBox[0]) + (BBox[3] - BBox[1]))
        step = perimeter_length / N
        coordinates = []
        current_position = 0
        for i in range(N):
            if current_position <= BBox[2] - BBox[0]:  # Top edge
                x = BBox[0] + current_position
                y = BBox[1]
            elif current_position <= (BBox[2] - BBox[0]) + (BBox[3] - BBox[1]):  # Right edge
                x = BBox[2]
                y = BBox[1] + (current_position - (BBox[2] - BBox[0]))
            elif current_position <= 2 * (BBox[2] - BBox[0]) + (BBox[3] - BBox[1]):  # Bottom edge
                x = BBox[2] - (current_position - (BBox[2] - BBox[0]) - (BBox[3] - BBox[1]))
                y = BBox[3]
            else:  # Left edge
                x = BBox[0]
                y = BBox[3] - (current_position - 2 * (BBox[2] - BBox[0]) - (BBox[3] - BBox[1]))
            coordinates.append((x, y))
            current_position += step
        return coordinates

- id: 8
  function_type: "coordinates"
  task_type: "Form a Circle"
  objective: "Agents form a circle around the center of the map."
  python_function: |
    def circle_formation(N: int, Objects: list, BBox: list[int]) -> list[tuple[int, int]]:
        import math
        center_x = (BBox[0] + BBox[2]) / 2
        center_y = (BBox[1] + BBox[3]) / 2
        radius = min(BBox[2] - BBox[0], BBox[3] - BBox[1]) / 4  # Circle radius is 1/4 of the smallest BBox dimension
        coordinates = []
        for i in range(N):
            angle = 2 * math.pi * i / N
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            coordinates.append((x, y))
        return coordinates

- id: 9
  function_type: "coordinates"
  task_type: "Form a Square"
  objective: "Agents form a square shape within the bounding box."
  python_function: |
    def form_square(N: int, Objects: list, BBox: list[int]) -> list[tuple[int, int]]:
        side_length = min((BBox[2] - BBox[0]), (BBox[3] - BBox[1])) / 2
        center_x = (BBox[0] + BBox[2]) / 2
        center_y = (BBox[1] + BBox[3]) / 2
        half_side = side_length / 2
        corners = [
            (center_x - half_side, center_y - half_side),
            (center_x + half_side, center_y - half_side),
            (center_x + half_side, center_y + half_side),
            (center_x - half_side, center_y + half_side)
        ]
        coordinates = []
        for i in range(N):
            corner = corners[i % 4]
            next_corner = corners[(i + 1) % 4]
            ratio = (i % (N // 4)) / (N // 4) if N >= 4 else 0
            x = corner[0] + ratio * (next_corner[0] - corner[0])
            y = corner[1] + ratio * (next_corner[1] - corner[1])
            coordinates.append((x, y))
        return coordinates

- id: 10
  function_type: "coordinates"
  task_type: "Form a Triangle"
  objective: "Agents form a triangle within the bounding box."
  python_function: |
    def form_triangle(N: int, Objects: list, BBox: list[int]) -> list[tuple[int, int]]:
        top_x = (BBox[0] + BBox[2]) / 2
        top_y = BBox[1]
        bottom_left = (BBox[0], BBox[3])
        bottom_right = (BBox[2], BBox[3])
        vertices = [bottom_left, bottom_right, (top_x, top_y)]
        coordinates = []
        for i in range(N):
            vertex1 = vertices[i % 3]
            vertex2 = vertices[(i + 1) % 3]
            ratio = (i % (N // 3)) / (N // 3) if N >= 3 else 0
            x = vertex1[0] + ratio * (vertex2[0] - vertex1[0])
            y = vertex1[1] + ratio * (vertex2[1] - vertex1[1])
            coordinates.append((x, y))
        return coordinates

- id: 11
  function_type: "coordinates"
  task_type: "Form the Letter 'L'"
  objective: "Agents form the letter 'L' shape inside the bounding box."
  python_function: |
    def form_letter_L(N: int, Objects: list, BBox: list[int]) -> list[tuple[int, int]]:
        height = BBox[3] - BBox[1]
        width = BBox[2] - BBox[0]
        vertical_count = N // 2
        horizontal_count = N - vertical_count
        coordinates = []
        for i in range(vertical_count):
            x = BBox[0]
            y = BBox[1] + i * (height / vertical_count)
            coordinates.append((x, y))
        for i in range(horizontal_count):
            x = BBox[0] + i * (width / horizontal_count)
            y = BBox[3]
            coordinates.append((x, y))
        return coordinates

- id: 12
  function_type: "coordinates"
  task_type: "Form the Letter 'T'"
  objective: "Agents form the letter 'T' shape inside the bounding box."
  python_function: |
    def form_letter_T(N: int, Objects: list, BBox: list[int]) -> list[tuple[int, int]]:
        vertical_count = N // 2
        horizontal_count = N - vertical_count
        height = BBox[3] - BBox[1]
        width = BBox[2] - BBox[0]
        coordinates = []
        # Vertical part
        for i in range(vertical_count):
            x = (BBox[0] + BBox[2]) / 2
            y = BBox[1] + i * (height / vertical_count)
            coordinates.append((x, y))
        # Horizontal part
        for i in range(horizontal_count):
            x = BBox[0] + i * (width / horizontal_count)
            y = BBox[1]
            coordinates.append((x, y))
        return coordinates

- id: 13
  function_type: "coordinates"
  task_type: "Form a Star"
  objective: "Agents form a star shape within the bounding box."
  python_function: |
    def form_star(N: int, Objects: list, BBox: list[int]) -> list[tuple[int, int]]:
        import math
        center_x = (BBox[0] + BBox[2]) / 2
        center_y = (BBox[1] + BBox[3]) / 2
        outer_radius = min((BBox[2] - BBox[0]), (BBox[3] - BBox[1])) / 3
        inner_radius = outer_radius / 2
        coordinates = []
        for i in range(N):
            angle = (i % 10) * math.pi / 5
            radius = outer_radius if i % 2 == 0 else inner_radius
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            coordinates.append((x, y))
        return coordinates

- id: 14
  function_type: "role"
  task_type: "Assign Scout and Leader"
  objective: "Assign roles to agents in an alternating pattern of scout and leader."
  python_function: |
    def assign_roles(N: int, Objects: list, BBox: list[int]) -> list[str]:
        roles = ["scout", "leader"]
        return [roles[i % 2] for i in range(N)]  # Alternating scout/leader

- id: 15
  function_type: "group"
  task_type: "Divide into Teams"
  objective: "Divide agents into two teams, alpha and beta, alternating between them."
  python_function: |
    def assign_groups(N: int, Objects: list, BBox: list[int]) -> list[str]:
        groups = ["alpha", "beta"]
        return [groups[i % 2] for i in range(N)]  # Alternating between groups

- id: 16
  function_type: "path"
  task_type: "Vertically Scan the Map"
  objective: "Agents move vertically along the map, scanning the area."
  python_function: |
    def spread_out_in_line_paths(N: int, Objects: list, BBox: list[int], steps: int) -> list[list[tuple[int, int]]]:

        Generate paths for N agents spreading out along the x-axis within the bounding box and moving vertically along the y-axis over time.

        Args:
            N: Number of agents.
            Objects: List of agents/objects to spread out (unused in this case but kept for future flexibility).
            BBox: Bounding box, defined as [x_min, y_min, x_max, y_max].
            steps: Number of steps (or time points) over which the agents move along the y-axis.

        Returns:
            A list of paths, where each path is a list of (x, y) coordinates representing the path of each agent over time.

        x_min, x_max = BBox[0], BBox[2]
        y_min, y_max = BBox[1], BBox[3]

        # Calculate the horizontal step to spread agents evenly along the x-axis
        x_step = (x_max - x_min) / (N - 1) if N > 1 else 0
        # Calculate the vertical step size for the y-axis based on the number of steps
        y_step = (y_max - y_min) / (steps - 1) if steps > 1 else 0

        # For each agent, generate a path of `steps` coordinates that move vertically over time
        paths = []
        for i in range(N):
            agent_x = x_min + i * x_step  # Fixed x position for each agent
            path = [(agent_x, y_min + step * y_step) for step in range(steps)]  # Vertical movement along y-axis
            paths.append(path)

        return paths
"""