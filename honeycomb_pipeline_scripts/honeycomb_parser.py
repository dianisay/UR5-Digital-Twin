import csv

class HoneycombParser:
    def __init__(self, scale_factor=0.001):
        # scale_factor defaults to 0.001 to convert mm to meters
        self.scale = scale_factor
        
    def parse_csv(self, filepath):
        """Reads (X, Y, Z) coordinates from a CSV file."""
        waypoints = []
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or row[0].startswith('#'): 
                    continue
                # Extract X, Y, Z
                x, y, z = float(row[0]), float(row[1]), float(row[2])
                # Scale to meters for the PyBullet physics environment
                waypoints.append([x * self.scale, y * self.scale, z * self.scale])
        return waypoints
        
    def generate_dummy_data(self, filepath="honeycomb_dummy.csv"):
        """Generates a mock coordinate file simulating your pipeline's output."""
        data = [
            [150.0, 200.0, 10.0],
            [160.0, 215.0, 10.0],
            [170.0, 215.0, 10.0],
            [180.0, 200.0, 10.0],
            [170.0, 185.0, 10.0],
            [160.0, 185.0, 10.0],
            [150.0, 200.0, 10.0]
        ]
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['# x(mm)', 'y(mm)', 'z(mm)'])
            writer.writerows(data)
        return filepath
