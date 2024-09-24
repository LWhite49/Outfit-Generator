const express = require("express");
const mongoose = require("mongoose");
const connectToMongoose = require("./connectMongoose.js");
const cors = require("cors");

// Import the route handlers
const {
	generateOutfitFeed,
	rateOutfit,
	deleteItem,
} = require("./controllers/outfitGenerationHandlers.js");

// Connect to MongoDB
connectToMongoose();

// Create App
const app = express();

// Middleware
app.use(express.json());
app.use(
	cors({
		origin: function (origin, callback) {
			// allow requests with no origin
			if (
				!origin ||
				origin.includes("wardrobewizard.app") ||
				origin.includes("localhost")
			) {
				return callback(null, true);
			} else {
				return callback(
					new Error(
						"The CORS policy for this site does not allow access from the specified Origin."
					)
				);
			}
		},
		methods: ["GET", "POST", "DELETE"],
	})
);

// Specify Routes
app.get("/generateOutfitFeed", generateOutfitFeed);
app.post("/rateOutfit", rateOutfit);
app.post("/deleteItem", deleteItem);

// Launch Server
const PORT = 3500;
app.listen(PORT, () => {
	console.log(
		"Server is running on port " +
			PORT +
			" at " +
			new Date().toLocaleTimeString()
	);
});
