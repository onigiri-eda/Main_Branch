CREATE DATABASE db_email_sender;
-- Table: email_lists (Stores email addresses and details)
CREATE TABLE email_lists (
  id SERIAL PRIMARY KEY
  , -- Auto-incrementing unique ID
    email VARCHAR(255) NOT NULL UNIQUE
  , -- Unique email address (required)
    name VARCHAR(255)
  , -- Optional name
    other_details TEXT -- Additional details (optional)
);

-- Table: email_templates (Stores email templates)
CREATE TABLE email_templates (
  id SERIAL PRIMARY KEY
  , -- Auto-incrementing unique ID
    subject VARCHAR(255) NOT NULL
  , -- Email subject (required)
    body TEXT NOT NULL -- Email body content (required)
);

INSERT INTO
  email_lists (email, name, other_details)
VALUES
  (
    'bubletea2246@gmail.com'
    , 'Bubble Tea Lover'
    , 'New Bubble Tea at Pizza Hut'
  )
  , (
    'gumball2013@mail.ru'
    , 'Gumball Fan'
    , 'General Promotion'
  )
  , (
    'pizzahut_enjoyer255@gmail.com'
    , 'Pizza Enthusiast'
    , 'New Bubble Tea at Pizza Hut'
  )
  , (
    'tamerlanbekbanov@gmail.com'
    , 'Tamerlan Bekbanov'
    , 'Glasses Promotion'
  )
  , (
    'tamerlanbekbanov2005@gmail.com'
    , 'Tamerlan Bekbanov'
    , 'New Laptop Promotion'
  )
  , (
    'bekbanotamerlan@gmail.com'
    , 'Tamerlan Bekbanov'
    , 'Glasses Promotion'
  )
  , (
    '35069@iitu.edu.kz'
    , 'IITU Student'
    , 'Midterm Week Warning'
  )
  , (
    'natsubmc@gmail.com'
    , 'Natsu BMC'
    , 'Fairy Tail Anime Update'
  )
  , (
    'natsubmc@icloud.com'
    , 'Natsu BMC'
    , 'Fairy Tail Anime Update'
  );

INSERT INTO
  email_templates (subject, body)
VALUES
  (
    '🍵 New Bubble Tea at Pizza Hut – Try It Today!'
    , 'Exciting news for all pizza and bubble tea lovers! 🍕🍵 Pizza Hut is introducing a brand-new Bubble Tea Menu featuring delicious flavors to pair with your favorite pizzas. Whether you love classic milk tea or fruity blends, we’ve got something special just for you. Visit your nearest Pizza Hut and be among the first to try this refreshing new addition! Don’t miss out—limited-time launch offer available!\n\nSee you soon at Pizza Hut!'
  )
  , (
    '👀 Upgrade Your Look with Stylish New Glasses!'
    , 'Hey Tamerlan,\n\nYour vision deserves the best! We’re excited to introduce our latest collection of stylish eyeglasses designed for comfort and clarity. Whether you need a fresh new look or a better fit for daily wear, we have the perfect pair waiting for you. For a limited time, enjoy 20% off your first purchase!\n\nDon’t wait—upgrade your style and see the world more clearly today!\n\n[Shop Now]'
  )
  , (
    '🚀 Your Next Laptop Upgrade is Here!'
    , 'Hi Tamerlan,\n\nLooking for a powerful and lightweight laptop? Our newest model is built for speed, performance, and portability—perfect for work, study, and gaming. Featuring the latest processor, a stunning display, and a long-lasting battery, this laptop is your perfect companion for any task.\n\nOrder now and enjoy an exclusive discount for early buyers!\n\n[Shop Now]'
  )
  , (
    '📢 Important: Midterm Week Starts Next Monday!'
    , 'Dear Student,\n\nThis is a reminder that Midterm Week is approaching! Exams will begin on Monday, and attendance is mandatory. Please check the university portal for your exam schedule and prepare accordingly.\n\nIf you have any questions, contact your department. Make sure to get enough rest and study well. Good luck!\n\nBest regards,\nIITU Administration'
  )
  , (
    '✨ Fairy Tail: Relive the Magic of the Guild!'
    , 'Hey Natsu,\n\nAre you ready for more Fairy Tail adventures? Whether you''re rewatching or catching up for the first time, now is the perfect time to dive back into the world of Natsu, Lucy, and the guild. Experience the epic battles, heartwarming friendships, and the magic that makes Fairy Tail legendary.\n\nJoin the guild once more—watch Fairy Tail today!\n\n[Start Watching]'
  );

ALTER TABLE email_lists
ALTER COLUMN email TYPE CITEXT;
ALTER TABLE email_templates
ADD CONSTRAINT body_not_empty CHECK (LENGTH(TRIM(body)) > 0);