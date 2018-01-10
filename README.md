# Hex Towns
This is the continuation of a group project, with bug fixes and new features. The original project which I contributed to can be found here: https://github.com/wshand/hex-towns

### <a name="members"></a>Team members
<a name="Team members"></a>
* GriffithGNeumark (Griffith Neumark)
* MoeMixMC (Mohamed Abdalla)
* codi2325 (Cody Luhmann)
* wshand (William Shand)

## <a name="instructions"></a>Instructions
In order to run this project, we recommend that you have at least version 3.6.0 of Python installed, as well as pip for Python 3.6.0.

* In order to view the code documentation, clone this repository, `cd` into `docs/documentation`, and open `index.html` in your browser.
* In order to execute the code for the game, first run `make build`. From then on, call `make run`.

## <a name="repository-organization"></a>Repository organization

The directory structure is roughly as follows (less important elements are removed for convenience):

    hex-towns/
    |-- src/
    |   |-- game/
    |   |   |-- game.py
    |   |   |-- player.py
    |   |   |-- gamefiles/
    |   |       |-- gamefile.py
    |   |       |-- games/
    |   |
    |   |-- map/
    |   |   |-- map.py
    |   |   |-- cell.py
    