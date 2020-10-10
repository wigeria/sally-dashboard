""" Provides common-ground between the API and Jobs for communicating
    via pubsub
"""


CHANNELS = {
    "completed_jobs": "completed_jobs"
}


def create_subscription(channel, handler, redis_instance):
    """ Creates a subscription for that channel on the redis instance and
        assigns it to the given handler

        Parameters
        ----------

        ``channel`` : string; A channel from redis_handler.CHANNELS

        ``handler`` : string; A handler function for messages on the channel

        ``redis_instance`` : redis.Redis ; Initialized redis instance

        Returns
        -------

        ``thread`` : Thread for the running subscription instance
    """
    assert channel in CHANNELS
    pubsub = redis_instance.pubsub()
    pubsub.psubscribe(**{CHANNELS[channel]: handler})
    return pubsub.run_in_thread(sleep_time=0.001)
