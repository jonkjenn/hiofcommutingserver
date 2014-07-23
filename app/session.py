def generate_key(self):
    import os, base64, random
                n = os.urandom(random.randint(15,25))
                        return base64.standard_b64encode(n)

