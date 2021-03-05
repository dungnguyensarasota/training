guess = 50
low = 0
high = 100
print("Please think of a number between 0 and 100!")
print("Is your secret number " + str(guess) + "?")
i = input("Enter 'h' to indicate the guess is too high. \
          Enter 'l' to indicate the guess is too low. \
           Enter 'c' to indicate I guessed correctly.")
ans = False
valid_response = ['c', 'h', 'l']
while ans != True:
    if i not in valid_response:
        print("Sorry, I did not understand your input.")
        print("Is your secret number " + str(guess) + "?")
        i = input("Enter 'h' to indicate the guess is too high. \
          Enter 'l' to indicate the guess is too low. \
           Enter 'c' to indicate I guessed correctly.")
    elif i == "h":
        high = guess
        guess = round((high + low) / 2)
        print("Is your secret number " + str(guess) + "?")
        i = input("Enter 'h' to indicate the guess is too high. \
          Enter 'l' to indicate the guess is too low. \
           Enter 'c' to indicate I guessed correctly.")
    elif i == "l":
        low = guess
        guess = round((high + low) / 2)
        print("Is your secret number " + str(guess) + "?")
        i = input("Enter 'h' to indicate the guess is too high. \
          Enter 'l' to indicate the guess is too low. \
           Enter 'c' to indicate I guessed correctly.")
    else:
        ans = True

print("Your secret number is " + str(guess))          
