MAX_COMMAND_PROCESSING = 100
"""The amount of commands the client can process at a time without responding.

This is already handleded internally so there is usually no need to use
this. You can think of the client managing a FIFO queue of command requests
with a capacity of 100. The client pops out the first entered command request
and sends a command response bback to the server. When the server tries to
send a command request while the queue is already full, then the command will
never be executed and an error will be sent by the client.

.. mermaid::
    :caption: An example of an interaction between the server and a client.

    %%{init: {'theme': 'dark'}}%%
    sequenceDiagram
        Server-)Client: Command Request
        Server-)Client: Command Request
        Server-)Client: Command Request
        Client-)Server: Command Response
        loop 98 times
            Server-)Client: Command Request
        end
        Server-xClient: Command Request
        loop 98 times
            Client-)Server: Command Response
        end
"""
