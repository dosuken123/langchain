def parse_numbered_list(input_str):
    lines = input_str.split("\n")
    parsed_list = []
    for line in lines:
        parts = line.split(". ", 1)
        if len(parts) == 2:
            index = int(parts[0])
            point = parts[1].strip()
            parsed_list.append({'point_index': index, 'point_skeleton': point})
    return parsed_list

def create_list_elements(_input):
    print(f"_input: {_input}")
    skeleton = _input['skeleton']
    numbered_list = parse_numbered_list(skeleton)
    for el in numbered_list:
        el['skeleton'] = skeleton
        el['question'] = _input['question']
    return numbered_list


if __name__ == "__main__":
    skeleton = """1. Clarify the issue.
2. Encourage open communication.
3. Actively listen to both parties.
4. Seek common ground.
5. Generate multiple solutions.
6. Negotiate and compromise.
7. Use a mediator if necessary.
8. Implement and follow-up on agreed resolutions.
9. Provide training on conflict resolution.
10. Foster a positive work environment.
"""

    print(parse_numbered_list(skeleton))