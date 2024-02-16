const mongoose = require('mongoose');
// Grab Schema class from mongoose
const Schema = mongoose.Schema;
// Create Schema for Men's Top collection
const topMenSchema = new Schema({
    productListing: {
        type: String,
        required: true
    },
    productImg: {
        type: String,
        required: true
    },
    productBrand: {
        type: String,
        required: true,
        index: true
    },
    productSize: {
        type: String,
        index: true
    },
    productColors: {
        type: [ String ], //Replace String with color object specifications, proabably as a subschema
        index: true
    },
    expiresAfter: {
        type: Date,
        required: true
    }
});

// Export the schema
module.exports = mongoose.model("TopMen", topMenSchema);