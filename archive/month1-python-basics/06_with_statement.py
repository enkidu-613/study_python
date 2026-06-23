class Door:
    def __enter__(self):
        print("open door")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("close door")


with Door() as door:
    print("enter door")
