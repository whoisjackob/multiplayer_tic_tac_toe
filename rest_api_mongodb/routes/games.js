const express = require('express');
const router = express.Router();

const Game = require('../models/Game');

router.get('/', async (req, res) => {
  try {
    const games = await Game.find()
      return res.send(games)
  } catch(error) {
      return res.send(error)
  }
});

router.post('/', async (req, res) => {
  try {
    const game = new Game({...req.body})
      await game.save()
      return res.send(game)
  } catch(error) {
      return res.send(error)
  }
});

router.get('/:id', async (req, res) => {
    try {
      const game = await Game.findById(req.params.id)
        return res.send(game)
    } catch(error) {
        return res.send(error)
    }
});

router.put('/:id', async (req, res) => {
    try {
      const id = req.params.id;
      await Game.findOneAndReplace({_id:id},{...req.body})
      return res.send({
        putGameId: id
      });
    } catch(error) {
        return res.send(error)
    }
});

router.delete('/:id', async (req, res) => {
  try {
    const id = req.params.id;
    await Game.deleteOne({ _id:id})
    return res.send({
      deletedGameId: id
    });
  } catch(error) {
      return res.send(error)
  } 
});

router.patch('/:id', async (req, res) => {
    try {
      const id = req.params.id;
      await Game.updateOne({_id:id},{...req.body});
      return res.send({
        //patchUserId: id
      });
    } catch(error) {
        return res.send(error)
    }
});

router.get('/:id/mqtt_backup', async (req, res) => {
    try {
      const game = await Game.find()
      const game2 = game[req.params.id]['mqtt_backup']
        return res.send(game2)
    } catch(error) {
        return res.send(error)
    }
});

// router.get('/:id/mqtt_backup', async (req, res) => {
//     try {
//       const game2 = await Game.find({'nr_chatu_priv': req.params.id})
//       console.log(game2);
//       return res.send(game2);
//     } catch(error) {
//         return res.send(error)
//     }
// });

router.get('/:id/0/mqtt_backup', async (req, res) => {
    try {
      const game2 = await Game.find({'nr_chatu_priv': req.params.id})
      return res.send(game2[0].mqtt_backup);
    } catch(error) {
        return res.send(error)
    }
});

router.patch('/:id/ogladajacy', async (req, res) => {
    try {
      const game = await Game.find()
      const game2 = game[req.params.id]
      const nowy = req.body
      console.log(game2)
      game2.ogladajacy.push(nowy.nowy)
      await game2.save()
      return res.send({
        addedCommentId: game2.ogladajacy.indexOf(nowy.nowy)
      });
    } catch(error) {
        return res.send(error)
    }
});

router.patch('/:id/mqtt_backup', async (req, res) => {
    try {
      const game2 = await Game.find({'nr_chatu_priv': req.params.id})
      const nowy = req.body
      console.log(game2)
      game2[0].mqtt_backup.push(nowy.nowy)
      await game2[0].save()
      return res.send({
        addedCommentId: game2[0].mqtt_backup
      });
    } catch(error) {
        return res.send(error)
    }
});


module.exports = router;
