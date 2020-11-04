import os
import discord
from discord.ext import commands
from discord.utils import get
from youtube import search, download, music_title
from time import sleep

video_choice = {}
song_queue = []


class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx = None

    @commands.command(pass_context=True, aliases=['p'])
    async def play(self, ctx, *, music):
        if str(ctx.channel) != 'music':
            return

        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        self.ctx = ctx
        global video_choice

        if voice is None:
            await channel.connect()
        elif voice and voice.is_connected():
            await voice.move_to(channel)

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                await ctx.send("Preparing song")
        except PermissionError:
            await ctx.send("Song is playing now. Your song will be in queue")
            global video_choice
            if music.isdigit():
                if int(music) > len(video_choice):
                    await ctx.send("Wrong option")
                    return
                else:
                    music = video_choice[int(music) - 1]

            video_choice = {}
            try:
                title = music_title(music)
                song_queue.append([title, music])
                await ctx.send("{} was placed in queue".format(title))
            except Exception as e:
                print(e)
                videos = search(music)
                embed = discord.Embed(title="Select song", color=0x0ff0ff)
                for i in range(len(videos)):
                    embed.add_field(name="** **", value="**{}**. {} | {}".format(i + 1, videos[i][3], videos[i][5]),
                                    inline=False)
                    video_choice[i] = videos[i][2]
                await ctx.send(embed=embed)
            return

        if music.isdigit():
            if int(music) > len(video_choice):
                await ctx.send("Wrong option")
                return
            else:
                music = video_choice[int(music)-1]

        video_choice = {}
        try:
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
        if str(ctx.channel) != 'music':
            return

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.pause()
            await ctx.send("Music paused")
        else:
            await ctx.send("Music not playing, I can`t pause")

    @commands.command(pass_context=True, aliases=['r', 'res'])
    async def resume(self, ctx):
        if str(ctx.channel) != 'music':
            return

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            voice.resume()
            await ctx.send("Music resumed")
        else:
            await ctx.send("Music is not paused")

    @commands.command(pass_context=True, aliases=['s'])
    async def stop(self, ctx):
        if str(ctx.channel) != 'music':
            return

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.stop()
            await ctx.send("Music stopped")
        else:
            await ctx.send("No music playing failed to stop")

    @commands.command(pass_context=True, aliases=['q'])
    async def queue(self, ctx, option='list', ind_1=-1, ind_2=-1):
        if str(ctx.channel) != 'music':
            return

        if option == 'delete':
            if len(song_queue) >= ind_1-1:
                music = song_queue[ind_1-1]
                song_queue.remove(music)
            else:
                await ctx.send("Bad index")
        elif option == 'set':
            if len(song_queue) >= ind_1-1 and len(song_queue) >= ind_2-1:
                music = song_queue[ind_1-1]
                song_queue.remove(music)
                song_queue.insert(ind_2-1, music)
            else:
                await ctx.send("Bad index")

        embed = discord.Embed(title="Song queue", color=0x0ff0ff)
        for i in range(len(song_queue)):
            embed.add_field(name="** **", value="**{}**. {}".format(i + 1, song_queue[i][0]), inline=False)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['n', 'nex', 'next'])
    async def next_song(self, ctx):
        if str(ctx.channel) != 'music':
            return

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.stop()
            sleep(0.5)
            song_there = os.path.isfile("song.mp3")
            if song_there:
                os.remove("song.mp3")
                await ctx.send("Preparing song")

            await ctx.send("Next Song")
            await ctx.send("Downloading music")
            music = song_queue[0]
            song_queue.remove(music)
            title = download(music[1])
            voice.play(discord.FFmpegPCMAudio("song.mp3"))
            await ctx.send("{} is playing now".format(title))
        else:
            await ctx.send("Join voice channel")
            return


def setup(bot):
    bot.add_cog(MusicPlayer(bot))
