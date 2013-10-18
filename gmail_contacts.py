#!/usr/bin/python

import sys
import getopt
import getpass
import atom
import gdata.contacts.data
import gdata.contacts.client

class ContactsSample(object):
    """ContactsSample object demonstrates operations with the Contacts feed."""

    def __init__(self, email, password):
        """Constructor for the ContactsSample object.

        Takes an email and password corresponding to a gmail account to
        demonstrate the functionality of the Contacts feed.

        Args:
          email: [string] The e-mail address of the account to use for the sample.
          password: [string] The password corresponding to the account specified by
              the email parameter.

        Yields:
          A ContactsSample object used to run the sample demonstrating the
          functionality of the Contacts feed.
        """
        self.gd_client = gdata.contacts.client.ContactsClient(source='GoogleInc-ContactsPythonSample-1')
        self.gd_client.ClientLogin(email, password, self.gd_client.source)

    def CreateMenu(self):
        """Prompts that enable a user to create a contact."""
        name = raw_input('Enter contact\'s name: ')
        notes = raw_input('Enter notes for contact: ')
        primary_email = raw_input('Enter primary email address: ')

        new_contact = gdata.contacts.data.ContactEntry(name=gdata.data.Name(full_name=gdata.data.FullName(text=name)))
        new_contact.content = atom.data.Content(text=notes)
        # Create a work email address for the contact and use as primary.
        new_contact.email.append(gdata.data.Email(address=primary_email,
                                                  primary='true', rel=gdata.data.WORK_REL))
        entry = self.gd_client.CreateContact(new_contact)

        if entry:
            print 'Creation successful!'
            print 'ID for the new contact:', entry.id.text
        else:
            print 'Upload error.'

    def CreateTestContactsMenu(self):
        """Prompts that enable a user to create a contact."""
        number = raw_input('Enter number of contact\'s you would like to create: ')

        for i in range(int(number)):
            name = 'test-account-' + str(i)
            primary_email = 'test.sugarone.' + str(i) + '@sugarcrm.com'
            title = 'Title for ' + name + ' contact'
            phone_number = '(206)555-1212'
            street = '1600 Amphitheatre Pkwy'
            city = 'Mountain View'
            region = 'CA'
            postcode = '94043'
            country = 'United States'
            notes = 'Test notes for ' + name + ' contact'
            image_filename = 'avatar.png'

            new_contact = gdata.contacts.data.ContactEntry(name=gdata.data.Name(full_name=gdata.data.FullName(text=name)))
            # Set the contact's postal address.
            new_contact.structured_postal_address.append(gdata.data.StructuredPostalAddress(rel=gdata.data.WORK_REL,
                                                                                            primary='true',
                                                                                            street=gdata.data.Street(text=street),
                                                                                            city=gdata.data.City(text=city),
                                                                                            region=gdata.data.Region(text=region),
                                                                                            postcode=gdata.data.Postcode(text=postcode),
                                                                                            country=gdata.data.Country(text=country)))
            # Set the contact's phone numbers.
            new_contact.phone_number.append(gdata.data.PhoneNumber(text=phone_number,
                                                                   rel=gdata.data.WORK_REL, primay='true'))
            # Set the contact's notes.
            new_contact.content = atom.data.Content(text=notes)
            # Set the contact's title
            new_contact.title = atom.data.Title(text=title)
            # Set the contact's email addresses.
            new_contact.email.append(gdata.data.Email(address=primary_email,
                                                      primary='true', rel=gdata.data.WORK_REL))
            entry = self.gd_client.CreateContact(new_contact)
            if i%10 == 0:
                self.gd_client.ChangePhoto(image_filename, entry, content_type='image/jpeg')

            if entry:
                print 'Creation successful!'
                print 'ID for the new contact:', entry.id.text
            else:
                print 'Upload error.'

    def PrintMenu(self):
        """Displays a menu of options for the user to choose from."""
        print ('\nContacts Sample\n'
               '1) Create a contact.\n'
               '2) Create set of contacts.\n'
               '0) Exit.\n')

    def GetMenuChoice(self, max):
        """Retrieves the menu selection from the user.

        Args:
          max: [int] The maximum number of allowed choices (inclusive)

        Returns:
          The integer of the menu item chosen by the user.
        """
        while True:
            input = raw_input('> ')

            try:
                num = int(input)
            except ValueError:
                print 'Invalid choice. Please choose a value between 0 and', max
                continue

            if num > max or num < 0:
                print 'Invalid choice. Please choose a value between 0 and', max
            else:
                return num

    def Run(self):
        """Prompts the user to choose funtionality to be demonstrated."""
        try:
            while True:

                self.PrintMenu()

                choice = self.GetMenuChoice(2)

                if choice == 1:
                    self.CreateMenu()
                elif choice == 2:
                    self.CreateTestContactsMenu()
                elif choice == 0:
                    return

        except KeyboardInterrupt:
            print '\nGoodbye.'
            return


def main():
    """Demonstrates use of the Contacts extension using the ContactsSample object."""
    # Parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ['user=', 'pw='])
    except getopt.error, msg:
        print 'python contacts_example.py --user [username] --pw [password]'
        sys.exit(2)

    user = ''
    pw = ''
    # Process options
    for option, arg in opts:
        if option == '--user':
            user = arg
        elif option == '--pw':
            pw = arg

    while not user:
        print 'NOTE: Please run these tests only with a test account.'
        user = raw_input('Please enter your username: ')
    while not pw:
        pw = getpass.getpass()
        if not pw:
            print 'Password cannot be blank.'


    try:
        sample = ContactsSample(user, pw)
    except gdata.client.BadAuthentication:
        print 'Invalid user credentials given.'
        return

    sample.Run()


if __name__ == '__main__':
    main()
