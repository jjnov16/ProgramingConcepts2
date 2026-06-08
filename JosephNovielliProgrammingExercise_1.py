def get_valid_ticket_count(remaining_tickets):
    """
    Function to prompt for and validate the user's input.
    Ensures the input is a valid number and within the allowed purchase limits.
    """
    while True:
        try:
            # Input: Prompting the user
            requested = int(input(f"Tickets remaining ({remaining_tickets}). How many tickets? (1-4)? "))

            # If statement: Check if the request exceeds valid bounds
            if requested < 1 or requested > 4:
                print("Invalid amount. You can only buy between 1 and 4 tickets.")
            elif requested > remaining_tickets:
                print(f"Not enough tickets left! You can only buy up to {remaining_tickets}.")
            else:
                return requested
        except ValueError:
            print("Please enter a valid whole number.")


def handle_ticket_sales():
    """
    Main loop function that processes ticket sales and manages the accumulators.
    """
    # Accumulators
    tickets_sold = 0
    total_buyers = 0
    total_tickets = 10

    # Loop: Run until all tickets are sold out
    while tickets_sold < total_tickets:
        remaining_tickets = total_tickets - tickets_sold

        # Call the input validation function
        tickets_to_buy = get_valid_ticket_count(remaining_tickets)

        # Update accumulators
        tickets_sold += tickets_to_buy
        total_buyers += 1

        # Output: Show remaining tickets
        print(f"-> You bought {tickets_to_buy} tickets. {total_tickets - tickets_sold} remaining.")

    # Output: Final display once sold out
    print("\n--- All Tickets Sold Out! ---")
    print(f"Total buyers: {total_buyers}")


# Run the program
if __name__ == "__main__":
    handle_ticket_sales()