import os
import discord
from discord.ext import commands
from discord.utils import get
from youtube import search, download, music_title, music_duration
from time import sleep
from config import BOT_PREFIX

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

        voice = get(self.bot.voice_clients, guild=ctx.guild)
        option = None
        try:
            if music[-1].isdigit() and music[-2] == '=' and music[-3] == ' ':
                option = int(music[-1])
                music = music[:-3]
        except Exception as e:
            print(e)
            if music.isdigit():
                if int(music) > len(video_choice):
                    await ctx.send("Wrong option")
                    return
                else:
                    music = video_choice[int(music) - 1]

        song_play = True
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                await ctx.send("Preparing song")
            song_play = False
        except PermissionError:
            await ctx.send("Song is playing now. Your song will be in queue")

        try:
            if int(music_duration(music)) < 800:
                if song_play:
                    title = music_title(music)
                    song_queue.append([title, music])
                    await ctx.send("{} was placed in queue".format(title))
                else:
                    title = download(music)
                    await ctx.send("{} is playing now".format(title))
                    voice.play(discord.FFmpegPCMAudio("song.mp3"))
            else:
                await ctx.send("Song too long")
        except Exception as e:
            print(e)
            if option is None:
                video_choice = {}
                videos = search(music)
                embed = discord.Embed(title="Select song", color=0x0ff0ff)
                for i in range(len(videos)):
                    embed.add_field(name="** **", value="**{}**. {} | {}".format(i + 1, videos[i][3], videos[i][5]),
                                    inline=False)
                    video_choice[i] = videos[i][2]
                await ctx.send(embed=embed)
            else:
                videos = search(music)
                for i in range(len(videos)):
                    video_choice[i] = videos[i][2]

                if option > len(video_choice):
                    await ctx.send("Wrong option")
                    return
                else:
                    music = video_choice[option - 1]

                if int(music_duration(music)) < 800:
                    if song_play:
                        title = music_title(music)
                        song_queue.append([title, music])
                        await ctx.send("{} was placed in queue".format(title))
                    else:
                        title = download(music)
                        await ctx.send("{} is playing now".format(title))
                        voice.play(discord.FFmpegPCMAudio("song.mp3"))
                else:
                    await ctx.send("Song too long")
        return

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
            elif ind_1 is None or ind_2 is None:
                await ctx.send("You should provide two numbers")
            else:
                await ctx.send("Bad index")

        if len(song_queue) > 0:
            embed = discord.Embed(title="Song queue", color=0x0ff0ff)
            for i in range(len(song_queue)):
                embed.add_field(name="** **", value="**{}**. {}".format(i + 1, song_queue[i][0]), inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("No music in queue")

    @commands.command(pass_context=True, aliases=['n', 'nex', 'next'])
    async def next_song(self, ctx):
        if str(ctx.channel) != 'music':
            return

        if len(song_queue) > 0:
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
            await ctx.send("No song in queue")

    @commands.command(pass_context=True, aliases=['h'])
    async def help(self, ctx):
        embed = discord.Embed(title="Music cog help", color=0x0ff0ff)
        embed.add_field(name="{}play".format(BOT_PREFIX),
                        value="play song, you should give url or name. Can be used with =1 tag", inline=False)
        embed.add_field(name="{}pause".format(BOT_PREFIX),
                        value="pause song, you can resume song with !resume command", inline=False)
        embed.add_field(name="{}resume".format(BOT_PREFIX),
                        value="resume song after !pause command", inline=False)
        embed.add_field(name="{}stop".format(BOT_PREFIX),
                        value="song can`t be resumed", inline=False)
        embed.add_field(name="{}next".format(BOT_PREFIX),
                        value="play next song in queue", inline=False)
        embed.add_field(name="{}queue".format(BOT_PREFIX),
                        value="show queue, can be used with 'delete {}' and 'set {} {}' tags", inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MusicPlayer(bot))
