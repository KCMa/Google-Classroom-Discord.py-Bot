import urllib.request
import json
import ssl
import discord


def fetchEnvData() -> dict:
    """Get the timetable from "https://iot.spyc.hk/spycenv"

    Returns:
        dict: dictionary containing all classes' timetable
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    with urllib.request.urlopen("https://iot.spyc.hk/spycenv") as url:
        results = url.read().decode()
        envData = json.loads(results)
        embedList=[]
        for env in envData:
          envEmbed=discord.Embed(title="{location}".format(**env), color=0xee8787)
          envEmbed.add_field(name="Temperature:", value="{temperature}°C".format(**env), inline=True)
          envEmbed.add_field(name="Relative humidity:", value="{relativeHumidity}%".format(**env), inline=True)
          envEmbed.add_field(name="Air pressure:", value="{airPressure}kPa".format(**env), inline=True)
          envEmbed.add_field(name="Last update:", value="{lastUpdate}".format(**env), inline=True)
          embedList.append(envEmbed)
        print(embedList)
        return embedList



if __name__ == "__main__":
    fetchEnvData()
