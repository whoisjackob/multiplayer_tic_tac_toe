const { Schema, model } = require('mongoose');

const gameSchema = new Schema({
    gracz1_name: String,
    gracz2_name: String,
    gracz1_lifes: Number,
    gracz2_lifes: Number,
    gracz1_choice: String,
    gracz2_choice: String,
    nr_chatu_priv: String,
    nr_chatu_pub: String,
    ogladajacy: Array,
    mqtt_backup: Array

});

module.exports = model('Game', gameSchema);