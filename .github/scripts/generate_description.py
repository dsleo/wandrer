import sys

def generate_description(activity_id, access_token):
    # You can use activity_id and access_token here if needed
    return "Good ride"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_description.py <activity_id> <access_token>")
        sys.exit(1)
    
    activity_id = sys.argv[1]
    access_token = sys.argv[2]
    description = generate_description(activity_id, access_token)
    print(description)
