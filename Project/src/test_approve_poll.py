from database import approve_poll

def main():
    poll_id_str = input("Enter poll id to approve: ")
    poll_id = int(poll_id_str)

    updated = approve_poll(poll_id)
    print("Approved poll:")
    print(updated)

if __name__ == "__main__":
    main()
