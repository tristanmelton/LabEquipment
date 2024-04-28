import matplotlib.pyplot as plot
from instruments.oscilloscopes.DS1104 import DS1104
import pandas as pd
import os

path = '230915_2'


scope = DS1104()
[time, tUnit, data1, data2, info] = scope.fetchData()
data = [time, tUnit, data1, data2, info]

plot.figure(1)
ax1 = plot.subplot(211)
plot.plot(time, data1)
plot.title("Channel 1")
plot.ylabel("Voltage (V)")
plot.xlabel("Time (" + str(tUnit) + ")")
plot.xlim(time[0], time[-1])
plot.subplots_adjust(hspace = 0.5)

plot.subplot(212, sharey=ax1)
plot.plot(time, data2)
plot.title("Channel 2")
plot.ylabel("Voltage (V)")
plot.xlabel("Time (" + str(tUnit) + ")")
plot.xlim(time[0], time[-1])

plot.show()

df = pd.DataFrame([time, data1, data2])
df.to_csv(os.path.join(path,f'Q_1056res.csv'),index=False)



