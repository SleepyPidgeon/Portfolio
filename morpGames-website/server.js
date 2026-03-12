const express = require('express');
const mongoose = require('mongoose');
const path = require('path');
const cors = require('cors'); // Importing CORS middleware
const app = express();
const ejs = require('ejs');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt'); // For password hashing
const crypto = require('crypto'); // For generating random passwords
const session = require('express-session');
const nodemailer = require('nodemailer');
const stringSimilarity = require('string-similarity');

// Middleware for CORS
app.use(cors({
    origin: 'http://127.0.0.1:5500',
    credentials: true // Allow cookies and credentials
}));

// Middleware for static files
app.use(express.static(path.join(__dirname, 'public'))); // Serve files from the `morpGames` directory




// Middleware for parsing requests
app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Session middleware
app.use(session({
    //Secret here is a placeholder
    secret: placeholder,
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: false, // Set to `true` if using HTTPS
        httpOnly: true,
        sameSite: 'Lax', // Required for cross-domain cookies
    },
}));

// MongoDB Connection, the connection is a placeholder
mongoose.connect('mongoserverhere', {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
    .then(() => {
        console.log('Connected successfully to MongoDB.');
    })
    .catch(err => {
        console.error('Error connecting to MongoDB:', err);
    });

// Root route
app.get('/', (req, res) => {
    res.send(`
        <h1>Server is Running</h1>
        <p>To access your application, open <a href="/Main.html">Main.html</a></p>
    `);
});

// Schemas
const leaderboardsSchema = {
    name: String,
    score: Number
};

const forumnSchema = {
    name: String,
    comment: String
};

const accountSchema = new mongoose.Schema({
    username: { type: String, required: true, unique: true },
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true },
    gold: { type: Number, default: 100 },
    scores: { type: Array, default: [] }
});

// Models
const morphouForum = mongoose.model('morphouF', forumnSchema, 'morphouF');
const rogueForum = mongoose.model('rougeF', forumnSchema, 'rougeF');
const sudokuForum = mongoose.model('sudokuF', forumnSchema, 'sudokuF');
const sliderForum = mongoose.model('sliderF', forumnSchema, 'sliderF');
const platformerForum = mongoose.model('platformerF', forumnSchema, 'platformerF');

const Score1 = mongoose.model('TimScores', leaderboardsSchema, 'TimScores');
const Score2 = mongoose.model('NewtonScores', leaderboardsSchema, 'NewtonScores');
const Score3 = mongoose.model('GabeScores', leaderboardsSchema, 'GabeScores');
const Score4 = mongoose.model('JesseScores', leaderboardsSchema, 'JesseScores');
const Score5 = mongoose.model('NatalyScores', leaderboardsSchema, 'NatalyScores');

const Accounts = mongoose.model('Accounts', accountSchema, 'Accounts');

// Routes
app.get('/leaderboards', async (req, res) => {
    try {
        const timScores = await Score1.find({}).sort({ score: -1 }).limit(5);
        const newtonScores = await Score2.find({}).sort({ score: -1 }).limit(5);
        const gabeScores = await Score3.find({}).sort({ score: -1 }).limit(5);
        const jesseScores = await Score4.find({}).sort({ score: -1 }).limit(5);
        const natalyScores = await Score5.find({}).sort({ score: -1 }).limit(5);

        res.render('leaderboards', {
            timScores,
            newtonScores,
            gabeScores,
            jesseScores,
            natalyScores
        });
    } catch (err) {
        console.error(err);
        res.status(500).send('Server Error');
    }
});

app.get('/forum', async (req, res) => {
    try {
        const morphouF = await morphouForum.find({}).sort({ _id: -1 }).limit(5);
        const rogueF = await rogueForum.find({}).sort({ _id: -1 }).limit(5);
        const sudokuF = await sudokuForum.find({}).sort({ _id: -1 }).limit(5);
        const sliderF = await sliderForum.find({}).sort({ _id: -1 }).limit(5);
        const platformerF = await platformerForum.find({}).sort({ _id: -1 }).limit(5);

        res.render('forum', { morphouF, rogueF, sudokuF, sliderF, platformerF });
    } catch (err) {
        console.error(err);
        res.status(500).send('Server Error');
    }
});

app.post('/post-comment', async (req, res) => {
    try {
        const { game, name, comment } = req.body;

        let forumModel;
        switch (game) {
            case 'morphouF':
                forumModel = morphouForum;
                break;
            case 'rougeF':
                forumModel = rogueForum;
                break;
            case 'sudokuF':
                forumModel = sudokuForum;
                break;
            case 'sliderF':
                forumModel = sliderForum;
                break;
            case 'platformerF':
                forumModel = platformerForum;
                break;
            default:
                return res.status(400).send('Invalid game selected');
        }

        const newComment = new forumModel({ name, comment });
        await newComment.save();
        res.redirect('/forum');
    } catch (err) {
        console.error(err);
        res.status(500).send('Server Error');
    }
});

app.get('/signup.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'Signup.html'));
});

app.post('/signup', async (req, res) => {
    try {
        const { username, email, password } = req.body;

        // Check if username or email already exists
        const existingUser = await Accounts.findOne({ $or: [{ username }, { email }] });
        if (existingUser) {
            return res.status(400).json({ error: 'Username or email already taken' });
        }

        // Hash password before saving
        const hashedPassword = await bcrypt.hash(password, 10);

        // Create new account
        const newAccount = new Accounts({ username, email, password: hashedPassword });
        await newAccount.save();
        res.status(201).json({ message: 'Signup successful!' });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Server error during signup' });
    }
});

// Login route
app.post('/login', async (req, res) => {
    const { username, password } = req.body;

    const user = await Accounts.findOne({ username });
    if (user && (await bcrypt.compare(password, user.password))) {
        req.session.username = username; // Set the session
        console.log('Session set:', req.session); // Debugging: Log the session
        res.json({ message: 'Login successful' });
    } else {
        res.status(401).json({ error: 'Invalid credentials' });
    }
});


// Endpoint to get the logged-in username
app.get('/user', (req, res) => {
    if (req.session && req.session.username) {
        console.log('Session data on /user:', req.session); // Debugging
        res.json({ username: req.session.username });
    } else {
        console.log('No session on /user request'); // Debugging
        res.status(401).json({ error: 'User not logged in' });
    }
});

app.get('/account', async (req, res) => {
    if (req.session && req.session.username) {
        try {
            // Fetch user details using async/await
            const user = await Accounts.findOne({ username: req.session.username });
            
            if (!user) {
                return res.status(404).json({ error: 'User not found' });
            }

            // Send back user details
            res.json({
                username: user.username,
                email: user.email,
                gold: user.gold,
            });
        } catch (err) {
            console.error('Error fetching user details:', err);
            res.status(500).json({ error: 'Failed to fetch account details' });
        }
    } else {
        res.status(401).json({ error: 'Unauthorized. Please log in.' });
    }
});



// Logout route
app.post('/logout', (req, res) => {
    if (req.session) {
        // Destroy the session
        req.session.destroy((err) => {
            if (err) {
                console.error('Error destroying session:', err);
                res.status(500).json({ error: 'Failed to log out' });
            } else {
                res.clearCookie('connect.sid'); // Clear the session cookie
                res.json({ message: 'Logout successful' });
            }
        });
    } else {
        res.status(400).json({ error: 'No session to log out' });
    }
});
// Forget Password route
app.post('/forgot-password', async (req, res) => {
    const { username, email } = req.body;

    try {
        // Find the user by email
        const user = await Accounts.findOne({ email });

        if (!user) {
            return res.status(404).json({ error: 'No account found with this email.' });
        }

        // Check if the provided username is close enough to the actual username
        const similarity = (str1, str2) => {
            let matches = 0;
            for (let i = 0; i < Math.min(str1.length, str2.length); i++) {
                if (str1[i].toLowerCase() === str2[i].toLowerCase()) matches++;
            }
            return matches / Math.max(str1.length, str2.length);
        };

        if (similarity(username, user.username) < 0.5) {
            return res.status(400).json({ error: 'Provided username does not match our records.' });
        }

        // Generate a new random password
        const newPassword = crypto.randomBytes(8).toString('hex');

        // Hash the new password
        const hashedPassword = await bcrypt.hash(newPassword, 10);

        // Update the password in the database
        user.password = hashedPassword;
        await user.save();

        // Set up the nodemailer transporter
        const transporter = nodemailer.createTransport({
            service: 'gmail',
            auth: {
                user: 'morpgames420@gmail.com', // Your email address
                pass: 'kekl hxpo anhy fgnz', // Your generated app password
            },
        });

        // Send the email with embedded image and fancy HTML
        const mailOptions = {
            from: '"Morp Games Support" <morpgames420@gmail.com>',
            to: email,
            subject: 'Password Reset - Morp Games',
            html: `
                <div style="font-family: Arial, sans-serif; color: #333; background-color: #f4f4f9; padding: 20px; border-radius: 10px; max-width: 600px; margin: 20px auto; text-align: center; border: 2px solid #00FF99;">
                    <h1 style="color: #00FF99; text-shadow: 0 0 5px #FF66CC;">Morp Games Password Reset</h1>
                    <p style="font-size: 16px; color: #555;">Hello <strong>${user.username}</strong>,</p>
                    <p style="font-size: 16px; color: #555;">Your password has been reset. Please use the new password below to log in:</p>
                    <div style="background-color: #222; color: #00FF99; padding: 15px; margin: 20px auto; font-size: 18px; border-radius: 5px; display: inline-block;">
                        <strong>${newPassword}</strong>
                    </div>
                    <p style="font-size: 16px; color: #555;">We recommend changing your password after logging in.</p>
                    <img src="cid:bigmorp@morpgames" alt="Morp" style="width: 200px; margin: 20px auto; display: block;">
                    <p style="font-size: 14px; color: #aaa;">If you did not request this password reset, please contact us immediately.</p>
                    <p style="font-size: 16px; color: #555;">Best regards,<br><strong>The Morp Games Team</strong></p>
                </div>
            `,
            attachments: [
                {
                    filename: 'bigmorp.png',
                    path: path.join(__dirname, 'public', 'img', 'bigmorp.png'), // Path to the image
                    cid: 'bigmorp@morpgames', // Content-ID for embedding
                },
            ],
        };

        await transporter.sendMail(mailOptions);

        res.status(200).json({ message: 'Password reset email sent successfully.' });
    } catch (error) {
        console.error('Error during password reset:', error);
        res.status(500).json({ error: 'An error occurred during password reset.' });
    }
});


// Change Password Route
app.post('/change-password', async (req, res) => {
    const { oldPassword, newPassword } = req.body;

    try {
        // Check if the user is logged in
        if (!req.session || !req.session.username) {
            return res.status(401).json({ error: 'You must be logged in to change your password.' });
        }

        // Find the user in the database
        const user = await Accounts.findOne({ username: req.session.username });

        if (!user) {
            return res.status(404).json({ error: 'User not found.' });
        }

        // Validate the old password
        const isPasswordValid = await bcrypt.compare(oldPassword, user.password);
        if (!isPasswordValid) {
            return res.status(400).json({ error: 'Current password is incorrect.' });
        }

        // Hash the new password
        const hashedPassword = await bcrypt.hash(newPassword, 10);

        // Update the password in the database
        user.password = hashedPassword;
        await user.save();

        res.status(200).json({ message: 'Password changed successfully.' });
    } catch (error) {
        console.error('Error during password change:', error);
        res.status(500).json({ error: 'An error occurred while changing the password.' });
    }
});



// Start the server
app.listen(3000, () => {
    console.log('Server is running on port 3000. Go to :::: http://localhost:3000/');
});
