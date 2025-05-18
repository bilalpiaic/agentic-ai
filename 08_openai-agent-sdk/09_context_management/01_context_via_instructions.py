from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

hotel_info = """
Welcome to the Grand Aurora Hotel, a prestigious five-star property situated in the vibrant downtown district of New Avalon. Our hotel redefines luxury through personalized service, elegant design, and modern functionality. Designed with both business travelers and leisure guests in mind, the Grand Aurora boasts 250 meticulously designed rooms, including 30 signature suites and 10 extended-stay luxury apartments. Every room features floor-to-ceiling windows, plush king or queen-size beds with premium linens, marble bathrooms, and complimentary high-speed Wi-Fi.

Our hotel is home to a host of world-class amenities designed to elevate every aspect of your stay. The on-site wellness center includes a fully equipped 24-hour gym, a heated indoor pool with hydrotherapy features, sauna and steam rooms, and the full-service Aurora Spa, offering signature massages, facials, and holistic treatments. We also offer wellness programs such as yoga, Pilates, and personal fitness training.

Dining is an experience at Grand Aurora. The rooftop restaurant "Celeste" offers breathtaking views of the city skyline and features a seasonal menu inspired by Mediterranean and Asian cuisines, made with locally-sourced, organic ingredients. Our bistro-style café "Terra Grounds" in the lobby serves freshly brewed coffee, artisanal pastries, and healthy snacks. “Velvet Bar” on the mezzanine level offers an extensive collection of wines, craft cocktails, and a curated selection of global tapas.

For corporate travelers, we provide over 10,000 square feet of event space, including a 500-seat grand ballroom, 8 customizable meeting rooms, and two executive boardrooms. Each space is equipped with high-speed internet, 4K projectors, wireless presentation systems, and hybrid meeting technology. Our dedicated events team handles everything from corporate retreats and product launches to weddings and social galas, with services including event planning, catering, décor, and technical support.

Our concierge team is available 24/7 to assist with transportation, dining reservations, city tours, and ticket bookings. We also offer complimentary airport transfers to Avalon International Airport, just 20 minutes away. For drivers, we provide valet parking, a self-parking garage, and charging stations for electric vehicles. Public transportation hubs and ride-sharing services are easily accessible from the hotel.

Families and long-term guests are well cared for. We offer babysitting services, children's welcome kits, cribs and roll-away beds, and kid-friendly menus. Our extended-stay suites come with kitchenettes, washer/dryers, and dedicated housekeeping. The hotel is pet-friendly and provides pet beds, food bowls, and pet-walking assistance on request.

Guest comfort is enhanced through smart room controls, including climate, lighting, and entertainment systems operated via touch panels or mobile apps. Rooms include HD smart TVs with streaming services, espresso machines, stocked mini-bars, in-room safes, blackout curtains, ergonomic workspaces, and twice-daily housekeeping.

Sustainability is at the heart of Grand Aurora’s philosophy. We use solar energy for water heating, motion-sensor lighting systems, organic and biodegradable toiletries, and a robust recycling and composting program. Our kitchen composts food waste and sources from regional farms to minimize our carbon footprint. Our sustainability efforts have earned us Green Globe Certification three years in a row.

Guests are encouraged to explore the charm of New Avalon. Located within walking distance of the hotel are key attractions such as the New Avalon Art Museum, Riverwalk Park, Central Market Street, and the historic Avalon Opera House. Our curated City Explorer packages include private guided tours, museum passes, and culinary experiences.

Room categories include:
- **Deluxe Rooms**: 350 sq ft, with garden or city views.
- **Executive Rooms**: Located on higher floors, with access to the Executive Lounge offering complimentary breakfast, evening cocktails, and private check-in.
- **Skyline Suites**: Featuring separate living areas, panoramic views, soaking tubs, and priority room service.
- **Presidential Suite**: A 2,000 sq ft private residence with a dining area, study, private spa room, and personal butler service.
- **Extended-Stay Apartments**: Fully furnished with living rooms, kitchens, laundry facilities, and weekly housekeeping—ideal for stays over 7 days.

Guests may check in from 3 PM and check out by 12 noon. Early check-in and late check-out are available on request based on availability. Breakfast is served daily from 6:30 AM to 10:30 AM in Celeste, and in-room breakfast is available upon request. Laundry, dry-cleaning, and express ironing are offered with same-day delivery. Business center services include printing, scanning, and virtual assistant support.

Security and privacy are paramount. The hotel is equipped with 24-hour surveillance, secure key-card access to all floors, and in-room safes. VIP guests and celebrities can request discrete check-in and use of the private elevator to the Executive Level. 

We host regular events such as jazz nights, wine tastings, art exhibitions in our in-house gallery, and Sunday brunches with live music. Loyalty program members receive exclusive benefits including upgrades, spa discounts, early check-in, and priority dining reservations.

At Grand Aurora Hotel, we are proud to merge the sophistication of urban living with the warmth of personalized hospitality. From the moment you arrive, every touchpoint has been thoughtfully curated to ensure your comfort, well-being, and delight. Whether you’re visiting for business, vacation, or celebration, we look forward to welcoming you to an unforgettable experience.

📍 **Address**: 88 Aurora Boulevard, Downtown New Avalon, Avalon City, 55678  
📞 **Phone**: +1 (555) 987-6543  
✉️ **Email**: contact@grandaurorahotel.com  
🌐 **Website**: www.grandaurorahotel.com  
📱 **Social Media**:  
- Instagram: @grandaurorahotel  
- Twitter: @AuroraLuxuryStay  
- Facebook: facebook.com/grandaurorahotel
"""

agent = Agent(
    name="Hotel Assistant",
    instructions="You are Grand Aurora Hotel Assistant" + hotel_info.strip(),
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
)

query = input("Ask your hotel-related question: ")

result = Runner.run_sync(
    agent,
    query,
)

print(result.final_output)
