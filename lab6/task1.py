# get the sender's name
sender = input('What is your name? ')

# get the transfer amount
transfer = float(input('How much do you want to e-transfer? '))

# get the recipient's name
receiver = input('Who is the recipient? ')

# get the security question
question = input('What is your security question? ')

# get the answer to the security question
security_answer = input('What is the security question\'s answer? ').lower()

# check if the receiver wants to accept the transaction
yn = input(f'{receiver}, you received {transfer} from {sender} via e-transfer, do you accept? ')

# if no, abort
if yn.lower() == 'n':
	print(f'{sender}, your e-transfer is declined by {receiver}.')
	exit()

# otherwise, ask for security question answer
answer = input(f'Security question: {question} ').lower()

# if it's wrong, abort
if answer != security_answer:
	print(f'Sorry, the security question\'s answer is wrong, the money is returned to {sender}.')
	exit()

# otherwise, transfer it
print('The security question\'s answer is correct, the money is deposit in your account.')
