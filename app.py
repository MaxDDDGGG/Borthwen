from flask import Flask, render_template, request, jsonify, redirect, url_for
import datetime
import urllib.request
import icalendar

app = Flask(__name__)

# SIMULATED DB FOR BOOKING>COM ETC
ROOMS = {
    "room1": {
        "name": "Double room (room 1)",
        "price": 1000,
        "capacity": 2,
        "images": ["room1_1.png", "room1_2.png", "room1_3.png"],
        "ical_url": ""
    },
    "Room 2": {
        "name": "Twin room (Room 2)",
        "price": 1000,
        "capacity": 2,
        "images": ["room2_1.png", "room2_2.png"],
        "ical_url": ""
    },
    "Room3": {
        "name": "Double room (room 3)",
        "price": 1000,
        "capacity": 2,
        "images": ["room3_1.png", "room3_2.png"],
        "ical_url": ""
    },
    "Room4": {
        "name": "Double room (room 4)",
        "price": 1000,
        "capacity": 2,
        "images": ["room4_1.png", "room4_2.png"],
        "ical_url": ""
    }
}

REVIEWS = [
    {
        "author": "A&K",
        "location": "Germany",
        "source": "Borthwen B&B",
        "rating": 5,
        "date": "July 2022",
        "text": "Immaculate and modern rooms, lovely breakfast, owners very welcoming. Such a peaceful setting only a 5 minute walk to Dolgellau centre, amazing views, off road parking Excellent and highly recommend."
    },
    {
        "author": "Suzanne and Mike",
        "location": "North West",
        "source": "Borthwen B&B",
        "rating": 5,
        "date": "May 2022",
        "text": "Warm, friendly and welcoming hosts, couldn't do enough for us during our stay. The B & B is recently renovated and 'immaculately' clean, every guest requirement catered for, even a blanket and bowl for dogs and large fridge under the stairs which was useful. The breakfast was first class, good quality produce, excellent selection and cooked to perfection."
    },
    {
        "author": "Donna Hooker",
        "location": "United Kingdom",
        "source": "Borthwen B&B",
        "rating": 5,
        "date": "May 2022",
        "text": "What a place!!! Both of the owners were so lovely! So friendly and personable! Really felt at ease here. The room was immaculate-with so many facilities! The freedom to come and go-and the recommendations of places to eat were great! The surroundings were beautiful and the breakfast was lovely!!"
    },
    {
        "author": "Jim & Claire",
        "location": "Essex",
        "source": "Borthwen B&B",
        "rating": 5,
        "date": "September 2021",
        "text": "We have just got back from 2 nights away, staying at Borthwen, and I couldn't recommend the B&B more. The welcome was so warm and friendly, the rooms are beautifully decorated, and the bed was so comfortable. Lastly, the breakfast, served to us in our room was arguably the best I have had in a long time."
    },
    {
        "author": "Sarah Parker",
        "location": "United Kingdom",
        "source": "Borthwen B&B",
        "rating": 5,
        "date": "August 2021",
        "text": "Comfortable, clean, welcoming, excellent breakfast, attention to detail, lovely view. Would definitely return."
    },
    {
        "author": "Geoff & Cathy Chesters",
        "location": "Redditch",
        "source": "Borthwen B&B",
        "rating": 5,
        "date": "August 2021",
        "text": "Myself and my wife Cathy stayed 2 nights at The Borthwen B&B. Our room was spotlessly clean, very comfortable bed and great views. The breakfasts were plentiful and tasty, and served on time. Would definitely recommend a stay there."
    },
    {
        "author": "Pallavi And Kalpesh Shingala",
        "location": "London",
        "source": "Borthwen B&B",
        "rating": 5,
        "date": "May 2021",
        "text": "Borthwen BnB exceeded our expectations in terms of facilities and the hygiene level they provide to their guests. We were warmly welcomed by Colin even though we reached after the check in time. Good quality breakfast was served to us in our rooms keeping C19 regulations into consideration."
    },
    {
        "author": "Allison & David",
        "location": "Basingstoke",
        "source": "Borthwen B&B",
        "rating": 5,
        "date": "July 2019",
        "text": "Stayed here for one night last week, My friend and i were on holiday travelling North Wales to shoot some pictures This is by far the best we stayed in .... superb location and stunning views Very warm and friendly welcome, lovely room and the most amazing breakfast (Black pudding) lush ..."
    }
]

def fetch_external_booked_dates(ical_url):
    """Fetches and parses iCal feeds from Booking.com or Airbnb to block booked dates."""
    booked_dates = []
    if not ical_url:
        return booked_dates
    try:
        with urllib.request.urlopen(ical_url, timeout=5) as response:
            kal = icalendar.Calendar.from_ical(response.read())
            for component in kal.walk():
                if component.name == "VEVENT":
                    start = component.get('dtstart').dt
                    end = component.get('dtend').dt
                    if isinstance(start, datetime.datetime):
                        start = start.date()
                    if isinstance(end, datetime.datetime):
                        end = end.date()
                    
                    curr = start
                    while curr < end:
                        booked_dates.append(curr.strftime("%Y-%m-%d"))
                        curr += datetime.timedelta(days=1)
    except Exception as e:
        print(f"Error syncing iCal feed: {e}")
    return booked_dates

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rooms')
def rooms():
    return render_template('rooms.html', rooms=ROOMS)

@app.route('/nearby')
def nearby():
    return render_template('nearby.html')

@app.route('/reviews')
def reviews():
    return render_template('reviews.html', reviews=REVIEWS)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        data = request.json
        return jsonify({"status": "success", "message": "Booking confirmed!", "details": data})
    return render_template('booking.html', rooms=ROOMS)

@app.route('/api/availability/<room_id>')
def get_availability(room_id):
    room = ROOMS.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404
    blocked_dates = fetch_external_booked_dates(room["ical_url"])
    return jsonify({"room": room["name"], "blocked_dates": blocked_dates})

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)