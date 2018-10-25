# timekeeper
Keeps an eye on working hours

I use Tasker on my Android phone to keep me updated on my working hours.
When I arrive I press a widget that writes the specific time to a .txt in my Dropbox and syncs it via DropSync. (I'm contemplating about if I should use 'connected to work WiFi/not' or an NFC chip instead of the widget.)
Same goes for break time, end break time, and departure.

Example file:
```
10-22-18 - 07.36
10-22-18 - 16.16
-
10-23-18 - 07.13
10-23-18 - 11.55
10-23-18 - 12.33
10-23-18 - 16.02

```
Note the new line at the end: new line is always added after, because that's the way the Tasker setting works.
Also note the '-' to separate days: The arrival function adds a dash, new line, and the timestamp. This to separate between days.

The python script then calculates my 'flex' (which is Swedish for flexible overtime), and writes it to another file in my Dropbox.

In the future I will add a function to send me an email every friday after work to tell me how much flex I have
