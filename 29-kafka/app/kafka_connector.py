from app.service import receve_msg_kafka
import aiokafka


async def getUserKafka():
    try:
        consumer = aiokafka.AIOKafkaConsumer("default", bootstrap_servers="host.docker.internal:29092")
        await consumer.start()

        async for msg in consumer:
            print("{}:{:d}:{:d}: key={} value={} timestamp_ms={}".format(msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp))
            await receve_msg_kafka(msg)    
    except Exception as ex:
        raise Exception(detail=str(ex))
    finally:
        await consumer.stop()     