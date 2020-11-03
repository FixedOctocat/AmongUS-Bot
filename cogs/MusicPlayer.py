import os
import shutil
import discord
from discord.ext import commands
from discord.utils import get
from youtube import search, download

video_choice = {}
song_queue = []


class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['p'])
    async def play(self, ctx, *, music):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice is None:
            await channel.connect()
        elif voice and voice.is_connected():
            await voice.move_to(channel)

        global video_choice
        if music.isdigit():
            if int(music) > len(video_choice):
                await ctx.send("Wrong option")
                return
            else:
                music = video_choice[int(music)-1]

        video_choice = {}
        try:
            song_there = os.path.isfile("song.mp3")
            try:
                if song_there:
                    os.remove("song.mp3")
                    await ctx.send("Preparing song")
            except PermissionError:
                await ctx.send("Song is playing now")
                return

            voice = get(self.bot.voice_clients, guild=ctx.guild)
            title = download(music)
            await ctx.send("Downloading music")
            await ctx.send("{} is playing now".format(title))
            voice.play(discord.FFmpegPCMAudio("song.mp3"))
        except Exception as e:
            print(e)
            videos = search(music)
            embed = discord.Embed(title="Select song", color=0x0ff0ff)
            for i in range(len(videos)):
                embed.add_field(name="** **", value="**{}**. {} | {}".format(i + 1, videos[i][3], videos[i][5]),
                                inline=False)
                video_choice[i] = videos[i][2]
            await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['pa', 'p_'])
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.pause()
            await ctx.send("Music paused")
        else:
            await ctx.send("Music not playing, I can`t pause")

    @commands.command(pass_context=True, aliases=['r', 'res'])
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            voice.resume()
            await ctx.send("Music resumed")
        else:
            await ctx.send("Music is not paused")

    @commands.command(pass_context=True, aliases=['s'])
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        queue_infile = os.path.isdir("./Queue")
        if queue_infile is True:
            shutil.rmtree("./Queue")

        if voice and voice.is_playing():
            print("Music stopped")
            voice.stop()
            await ctx.send("Music stopped")
        else:
            print("No music playing failed to stop")
            await ctx.send("No music playing failed to stop")

    @commands.command(pass_context=True, aliases=['n', 'nex', 'next'])
    async def next_song(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.stop()
            await ctx.send("Next Song")
        else:
            await ctx.send("No music in queue")


def setup(bot):
    bot.add_cog(MusicPlayer(bot))
