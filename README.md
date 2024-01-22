# Workouts with Body Tracking
The **workouts-with-body-tracking** project is designed to enhance the experience of physical exercise through the use of body tracking techniques. Each directory in this repository contains specific `README.md` information about configurations and scripts related to body tracking, facilitating the integration of these tools into your fitness routine.

## Repository Structure

```
workouts-with-body-tracking/
── exercise_one/
│ ├── README.md
│ ├── exercise_one.py
│ └── ...
├── exercise_two/
│ ├── README.md
│ ├── exercise_two.py
│ └── ...
└── ...
```

Cada pasta contém os seguintes elementos:

## How to Use

To use a script, see the `README.md` file in the corresponding exercise folder. `README.md` will provide instructions for what it is for and step-by-step instructions on how to configure and run the script.

## Get started

<details>
  <summary><strong>Make sure you have Python 3.3 or later and pip installed on your machine</strong></summary><br />
  
* To check if you have `python` and `pip`
  ```bash
  python3 --version && pip --version
  ```
* The output should be similar to something like this
  ```
  Python 3.8.10
  pip 20.0.2 from /usr/lib/python3/dist-packages/pip (python 3.8)
  ```
</details>

<br>

1. Make a clone of the repository and enter it

```bash
git clone git@github.com:luandersonalvesdev/workout-with-body-tracking.git
cd workout-with-body-tracking
```

2. Create a separate virtual environment with `venv`

```bash
python3 -m venv environment_name
```

3. Activate the virtual environment

- Windows:
    ```bash
    environment_name\Scripts\activate
    ```

- Linux:
    ```bash
    source environment_name/bin/activate
    ```

4. Install dependencies from `dev-requirements.txt`
```bash
pip install -r dev-requirements.txt
```

6. Ready! Just run any script
```bash
python exercise_one/exercise_one.py
```

## Contribuições

This project welcomes contributions from the community. If you want to add a new script not included or enhance an existing script, feel free to *fork* this repository, make the necessary changes, and submit a *pull request*.

---

*This project is maintained by Luanderson Alves and contributors. To contact me, send an email to **[luaoderson@gmail.com]** or you can also find me on [Linkedin](https://www.linkedin.com/in/luandersonalvesdev/).*