from pathlib import Path
import string, random, json, re

class bank:
    source = 'data.json'
    data = []

    try:
        if Path(source).exists():
            with open('data.json') as fs:
                data = json.loads(fs.read())
        else:
            print('data file not exists!')    
    except Exception as err:
        print(err)

    @staticmethod
    def __update():
        with open(bank.source,'w') as fs:
            fs.write(json.dumps(bank.data))

    def create(self):
        details = {
            'name': input('Enter ur name: '),
            'email': input('Enter ur email: ').strip().lower(),
            'pin': int(input('Generate 4-digit pin: ')),
            'bal':int(input('Deposit atleast 10k to create account: '))
        }
        # account and email duplicate checker
        existing_emails = {account['email'].lower() for account in bank.data}
        existing_accounts = {account['acc'] for account in bank.data}
        details['acc'] = random.randint(10000, 99999)
        while details['acc'] in existing_accounts:
            details['acc'] = random.randint(10000, 99999)

        # Pin validation
        if len(str(details['pin'])) != 4:
            print('Please enter a valid 4-digit pin')
        elif details['bal'] < 10000:
            print('deposit atleast 10k!')    
        # email validation
        elif not re.fullmatch(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', details['email']):
            print('Please enter a valid email address')
        elif details['email'] in existing_emails:
            print('That email is already registered')
        else:
            for i in details:
                print(f"{i} : {details[i]}")
            print('Account created successfully, please note-down ur account details')
            bank.data.append(details)
            bank.__update()

    def deposit(self):
        acc = int(input('Enter ur account number: '))
        pin = int(input('Enter ur account pin: '))

        info = [inf for inf in bank.data if inf['acc'] == acc and inf['pin'] == pin]

        if not info:
            print('U have entered wrong creds!, enter carefully and try again.')

        else:    
            bal = int(input('Enter amount u want to deposit number: '))

            if bal > 100000 and bal < 500:
                print('please do not deposit too huge and small amount.')
            else:
                info[0]['bal'] += bal
                bank.__update()
                print("Amount deposited successfully ")
                print(f"Available balance: {info[0]['bal']} ")

    def withdraw(self):
        acc = int(input('Enter ur account number: '))
        pin = int(input('Enter ur account pin: '))

        info = [inf for inf in bank.data if inf['acc'] == acc and inf['pin'] == pin]

        if not info:
            print('U have entered wrong creds!, enter carefully and try again.')

        else:    
            bal = int(input('Enter amount u want to withdraw number: '))

            if info[0]['bal'] < bal:
                print('Insufficient balance!')
                print(f"Available balance: {info[0]['bal']} ")
            else:
                info[0]['bal'] -= bal
                bank.__update()
                print("Amount withdraw successfully ")
                print(f"Available balance: {info[0]['bal']} ")

    def viewdetails(self):
        acc = int(input('Enter ur account number: '))
        pin = int(input('Enter ur account pin: '))
    
        info = [inf for inf in bank.data if inf['acc'] == acc and inf['pin'] == pin]
    
        if not info:
            print('U have entered wrong creds!, enter carefully and try again.')
    
        else:    
            print('---Account Details---')
            for inf in info[0]:
                print(f"{inf}: {info[0][inf]}")        

    def updatedetails(self):
        acc = int(input('Enter ur account number: '))
        pin = int(input('Enter ur account pin: '))
    
        info = [inf for inf in bank.data if inf['acc'] == acc and inf['pin'] == pin]
    
        if not info:
            print('U have entered wrong creds!, enter carefully and try again.')
    
        else:    
            print('Account Number and Balance not updateable')
            print('N/n -> name, E/e -> email, P/p -> pin')
            print('Enter one or more choices, for example: nep or n,e,p')
            edit = set(input('What u want to update: ').lower().replace(',', '').replace(' ', ''))
            account = info[0]

            if not edit or not edit.issubset({'n', 'e', 'p'}):
                print('Select valid details to update')
                return

            updates = {}
            if 'e' in edit:
                mail = input('Enter Update email: ').strip().lower()
                existing_emails = {
                    item['email'].lower() for item in bank.data if item is not account
                }
                if not re.fullmatch(
                    r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', mail
                ):
                    print('Please enter a valid email address')
                    return
                elif mail in existing_emails or mail == account['email'].lower():
                    print('That email is already registered')
                    return
                updates['email'] = mail

            if 'n' in edit:
                name = input('Enter Update name: ').strip()
                if not name:
                    print('Name cannot be empty')
                    return
                elif name == account['name']:
                    print('New name must be different from the previous name')
                    return
                updates['name'] = name

            if 'p' in edit:
                new_pin = input('Enter Update pin: ').strip()
                if not new_pin.isdigit() or len(new_pin) != 4:
                    print('Please enter a valid 4-digit pin')
                    return
                updates['pin'] = int(new_pin)

            account.update(updates)
            bank.__update()
            print('Account details updated successfully')

    def deleteaccount(self):
        acc = int(input('Enter ur account number: '))
        pin = int(input('Enter ur account pin: '))

        info = [inf for inf in bank.data if inf['acc'] == acc and inf['pin'] == pin]

        if not info:
            print('U have entered wrong creds!, enter carefully and try again.')
            return

        res = input('Are u want to delete account? (y/n): ').strip().lower()
        if res == 'y':
            bank.data.remove(info[0])
            bank.__update()
            print('Account deleted successfully')
        elif res == 'n':
            print('Account was not deleted')
        else:
            print('Please enter y or n')

bank1 = bank()

print('1 - for create an account')
print('2 - for deposit money')
print('3 - for withdraw money')
print('4 - for account details')
print('5 - for update account details')
print('6 - for delete an Account')

opt = int(input('Enter ur response: '))

if opt == 1:
    bank1.create()
elif opt == 2:
    bank1.deposit()
elif opt == 3:
    bank1.withdraw()
elif opt == 4:
    bank1.viewdetails()
elif opt == 5:
    bank1.updatedetails()
elif opt == 6:
    bank1.deleteaccount()
else:
    print('Select wrong options!')