import ray


@ray.remote
def process_video():
    print("Running my data processing pipeline!")
    return "Success"


obj_ref = process_video.remote()
ray.get(obj_ref)
