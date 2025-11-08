# NFC Utils

As set of Python-based tools used for working with audio files and the results files of Nighthawk and BirdNET analysis engines. These tools aim for compatibility across Windows, GNU/Linux, and MacOS.

## Listing Utility

### Requirements

* Read and process all uncompressed WAV files natively (need to compare performane to wave library)
* Read and process both Nighthawk and BirdNET detections files
* Be NFC aware (given a set of GPS coordinates)
* Output unified detections in a standardized format based on common fields
* Extract audio clips from WAV files
* Generate spectrograms of audio clips
* Display time table (sunrise/sunset, twilight, astronomical twilight) for a given date (default current date)
* Ability to specify custom filename format (e.g., NNNN_YYYYMMDD_HHMMSS-ZZ)
* Display detections in tabular format (like 'll' in Linux)
* Filter detections by: species, confidence level
* Read configuration from an INI file
* Generate unified Audacity labels (e.g., one Audacity labels file for all analysis engines)

### Enhancements

* Support FLAC audio format (use native libraries)
* Support JSON output of detections and WAV metadata
* Capture WAV metadata and detections in a database for advances processing
* Ability to repair WAV files which were truncated (e.g., power outage)

## Recording Utility

### Requirements

* Record in WAV format
* Read configuration from an INI file (default: ./)
* Record {{ duration }} continuously (e.g., record 1-hour chunks forever)
* Ability to run as a background process (e.g., system daemon in linux)
* Delay recording until a certain time (e.g., don't start until sunset, twilight, astro-twilight, etc)
* Align recordings to nearest time unit (e.g., start recording at the top of the hour when recording in 60 minute intervals)
* Allow custom filename patterns

### Enhancements

* Ability to record for different durations for different protocols (e.g., diurnal, nocturnal, nfc)
* Record in FLAC format
* Capture weather information
* Capture moon phase
* Write all metadata (e.g., WAV, weather, moon phase) to JSON

### Issues

* Need to recalculate time/tz before each new recording chunk (to handle daylight saving time changing)
