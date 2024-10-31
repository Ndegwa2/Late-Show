import csv
from app import app, db
from models import Episode, Guest, Appearance

def populate_database():
    with app.app_context():
        # Remove existing data in the proper sequence to maintain database integrity
        print("Removing existing records...")
        db.session.query(Appearance).delete()
        db.session.query(Episode).delete()
        db.session.query(Guest).delete()
        db.session.commit()

        print("Loading data from the CSV file...")

        # Open and read the CSV data
        with open('seed.csv', newline='') as csvfile:  # Make sure the file path is accurate
            data_reader = csv.DictReader(csvfile)
            
            guest_dictionary = {}  # Cache to hold existing guests and avoid duplicates

            for entry in data_reader:
                name = entry['Raw_Guest_List']
                occupation = entry['GoogleKnowlege_Occupation']
                show_date = entry['Show']
                year = int(entry['YEAR'])

                # Check for guest existence to avoid duplication
                if name not in guest_dictionary:
                    new_guest = Guest(name=name, occupation=occupation)
                    db.session.add(new_guest)
                    db.session.flush()  # Ensures ID is generated for the new guest
                    guest_dictionary[name] = new_guest.id
                else:
                    guest_id = guest_dictionary[name]
                    new_guest = Guest.query.get(guest_id)

                # Create a new episode instance
                new_episode = Episode(date=show_date, number=year)
                db.session.add(new_episode)
                db.session.flush()  # Ensures ID is generated for the new episode

                # Create a new appearance relationship
                new_appearance = Appearance(rating=3, episode_id=new_episode.id, guest_id=new_guest.id)
                db.session.add(new_appearance)

            db.session.commit()
            print("Database seeding is complete!")

if __name__ == '__main__':
    populate_database()
