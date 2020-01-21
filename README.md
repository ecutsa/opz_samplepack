# opz_samplepack

![](http://aqhlt.fr/img/opz_demo.gif)

Launch the script inside a folder full of samples and it will returns you samplespacks !

## how it works:
actually it scans all .wav files in the current folder and create samplepacks of 24 samples separated inside differents folders 

## Install

### Step 1: Install operating system requirements
##### linux
```aptitude install python3 ffmpeg```

##### macOS 
Requirements:

- You need Xcode to install brew:
  ```
  xcode-select --install
  ```
- You need brew to install python 3:
  ```
  /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  ```
- You need python 3 and ffmpeg to use this wonderfull software:
  ```
  brew install python3 ffmpeg
  ```
##### Windows:
I don't have any windows to test it. Feedback appreciated.

### Step 2: Install python3 dependencies

You will need 2 awesome python dependencies to generate samplepacks, here is how to install them:
```python
pip3 install librosa audiosegment
```

### Step 3: Use the software
- put the script in a folder full of samples
- run it ( https://youtu.be/tRoomSW0900 )
- copy the generated samplepack(s) in a drum slot of your opz
- enjoy :)


