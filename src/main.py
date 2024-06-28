# flake8: noqa: F403, F405
# pylint: disable=undefined-variable, unused-argument, unused-wildcard-import
import logging
import os

from src.bedrock.server import Server
from src.bedrock.game_context import *
from src.bedrock.game_context_factory import get_all_game_events
from src.bedrock.server_context import *


def setup_server_events(app: Server):
    @app.server_event
    async def ready(ctx: ReadyContext) -> None:
        print(f'Ready @ {ctx.host}:{ctx.port}')
        print(f'run /connect {ctx.host}:{ctx.port} in Minecraft to connect to this server')

    @app.server_event
    async def connect(ctx: ConnectContext) -> None:
        print('Connected: player')

    @app.server_event
    async def disconnect(ctx: DisconnectContext) -> None:
        print('Disconnected: player')


def setup_game_events(app: Server):
    # pylint: disable=too-many-locals
    @app.game_event
    async def block_broken(ctx: BlockBrokenContext) -> None:
        print(f'{ctx.player.name} broke {ctx.count} {ctx.block.namespace}:{ctx.block.id} with "{ctx.tool.id}"')

    @app.game_event
    async def block_placed(ctx: BlockPlacedContext) -> None:
        print(f'{ctx.player.name} placed {ctx.count} {ctx.block.namespace}:{ctx.block.id}')

    @app.game_event
    async def chunk_changed(ctx: ChunkChangedContext) -> None:
        print(f'Chunk changed {ctx.chunk}')

    @app.game_event
    async def chunk_loaded(ctx: ChunkLoadedContext) -> None:
        print(f'Chunk loaded {ctx.chunk}')

    @app.game_event
    async def chunk_unloaded(ctx: ChunkUnloadedContext) -> None:
        print(f'Chunk unloaded {ctx.chunk}')

    @app.game_event
    async def end_of_day(ctx: EndOfDayContext) -> None:
        print('End of day')

    @app.game_event
    async def entity_interacted(ctx: EntityInteractedContext) -> None:
        print(f'Entity interacted')

    @app.game_event
    async def entity_spawned(ctx: EntitySpawnedContext) -> None:
        print(f'Entity spawned')

    @app.game_event
    async def item_acquired(ctx: ItemAcquiredContext) -> None:
        print('Item acquired')

    @app.game_event
    async def item_crafted(ctx: ItemCraftedContext) -> None:
        print('Item crafted')

    @app.game_event
    async def item_dropped(ctx: ItemDroppedContext) -> None:
        print('Item dropped')

    @app.game_event
    async def item_equipped(ctx: ItemEquippedContext) -> None:
        print(f'Item equipped {ctx.item.namespace} : {ctx.item.id} by {ctx.player.name} @ {ctx.player.position}')

    @app.game_event
    async def item_interacted(ctx: ItemInteractedContext) -> None:
        print('Item interacted')

    @app.game_event
    async def item_used(ctx: ItemUsedContext) -> None:
        print(f'Item used {ctx.item.namespace} : {ctx.item.id} by {ctx.player.name} @ {ctx.player.position}')

    @app.game_event
    async def mob_interacted(ctx: MobInteractedContext) -> None:
        print(f'Mob interacted {ctx.mob.type} with player: {ctx.player.name} @ {ctx.player.position}')

    @app.game_event
    async def mob_killed(ctx: MobKilledContext) -> None:
        print('Mob killed')

    @app.game_event
    async def player_bounced(ctx: PlayerBouncedContext) -> None:
        print(f'Player bounced {ctx.player.name} on {ctx.block.namespace}:{ctx.block.id} with height {ctx.bounce_height}')

    @app.game_event
    async def player_died(ctx: PlayerDiedContext) -> None:
        print(f'player_died {ctx.player.name} @ {ctx.player.position}')

    @app.game_event
    async def player_join(ctx: PlayerJoinContext) -> None:
        print(f'player_joined {ctx.player.name} @ {ctx.player.position}')

    @app.game_event
    async def player_leave(ctx: PlayerLeaveContext) -> None:
        print('player_left')

    @app.game_event
    async def player_message(ctx: PlayerMessageContext) -> None:
        print(f'{ctx.sender}: {ctx.message}')
        if ctx.message == 'hello':
            await ctx.reply('hi')

    @app.game_event
    async def player_teleported(ctx: PlayerTeleportedContext) -> None:
        print('player_teleported', ctx.player.name, ctx.player.position)

    @app.game_event
    async def player_transform(ctx: PlayerTransformContext) -> None:
        print('player_transformed', ctx.player.name, ctx.player.position)

    @app.game_event
    async def player_travelled(ctx: PlayerTravelledContext) -> None:
        print('player_travelled', ctx.player.name, ctx.player.position)


def main():

    host = os.getenv('HOST', 'localhost')
    port = int(os.getenv('PORT', 6464))

    logging.basicConfig(level=logging.INFO)

    app = Server()

    setup_server_events(app)

    setup_game_events(app)

    app.start(host, port)
    input('Press enter to close the server')
    app.close()


if __name__ == '__main__':
    main()
