const express = require('express');
const mongoose = require('mongoose');
const connectToMongoose = require('./connectMongoose.js');
const cors = require('cors');


// Import the route handlers
const { generateRandomOutfits, generateRandomOutfitsByBrand } = require('./controllers/outfitGenerationHandlers.js');

// Connect to MongoDB
connectToMongoose();

// Create App
const app = express();

// Middleware
app.use(express.json());
app.use(cors());

// Specify Routes
app.get("/getRandomOutfits", generateRandomOutfits);
app.get("/getRandomOutfitsByBrand", generateRandomOutfitsByBrand);

// Launch Server
const PORT = 3500;
app.listen(PORT, () => {console.log("Server is running on port " + PORT + " at " + new Date().toLocaleTimeString())});

