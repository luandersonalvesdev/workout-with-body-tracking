# Squat counter

The squat_counter script is a body tracking application that includes a squat counting feature along with a timer to assist in exercises. Squats are counted when the hip's line on both sides goes below the knee line. The directory consists of the `squat_counter.py` script and a configuration file `config.json` containing three variables:

```json
{
  "acceptance_range_for_squats": 40,
  "is_show_squat_range_line": true,
  "is_show_body_tracking_line": true,
}
```
  - **acceptance_range_for_squats**: Defines an acceptable limit for squats. In cases where the camera angle is not optimal, you can configure it to count squats even if they do not pass below the knee line.
  - **is_show_squat_range_line**: A boolean indicating whether the user wants the line representing the acceptable limit to be displayed or not.
  - **is_show_body_tracking_line**: A boolean indicating whether the user wants the body tracking lines to be displayed or not.

## To use

If you have followed all the instructions provided in the initial [README.md](https://github.com/luandersonalvesdev/workout-with-body-tracking), you are now ready to use this script. Just run the script with python.
```bash
python squat_counter.py
```