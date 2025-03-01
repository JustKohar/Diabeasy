const mongoose = require('mongoose');

const InsulinScaleSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  timeOfDay: { type: String, required: true }, // e.g., "morning", "afternoon", "evening"
  bloodSugarRange: { type: String, required: true }, // e.g., "150-200"
  insulinDose: { type: Number, required: true }, // e.g., 2 units
});

module.exports = mongoose.model('InsulinScale', InsulinScaleSchema);