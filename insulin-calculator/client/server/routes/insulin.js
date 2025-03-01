const express = require('express');
const InsulinScale = require('../models/InsulinScale');
const router = express.Router();

// Save or update insulin scale
router.post('/scale', async (req, res) => {
  const { userId, timeOfDay, bloodSugarRange, insulinDose } = req.body;
  const scale = new InsulinScale({ userId, timeOfDay, bloodSugarRange, insulinDose });
  await scale.save();
  res.status(201).send('Scale saved');
});

// Get insulin dose based on time of day and blood sugar
router.get('/calculate', async (req, res) => {
  const { userId, timeOfDay, bloodSugar } = req.query;
  const scale = await InsulinScale.findOne({ userId, timeOfDay });
  if (scale) {
    const [min, max] = scale.bloodSugarRange.split('-').map(Number);
    if (bloodSugar >= min && bloodSugar <= max) {
      res.status(200).json({ dose: scale.insulinDose });
    } else {
      res.status(404).send('No matching scale found');
    }
  } else {
    res.status(404).send('Scale not found');
  }
});

module.exports = router;