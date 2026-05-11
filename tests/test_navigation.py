"""Test bidirectional exits on all floor modules."""
import sys, os, importlib

def test_floor(floor_num):
    """Test bidirectional exits for one floor."""
    try:
        mod = importlib.import_module(f"floors.floor_{floor_num}")
    except ImportError:
        return None, f"Module not found"
    
    rooms = getattr(mod, "ROOMS", None)
    if not rooms:
        return None, "No ROOMS dict"
    
    errors = []
    for room_id, room in rooms.items():
        exits = room.get("exits", {})
        for direction, target in exits.items():
            if target == 0 or target is None:
                continue
            # Skip inter-floor transitions (string markers like "floor_9", "floor_7", etc.)
            if isinstance(target, str):
                continue
            if target not in rooms:
                errors.append(f"Room {room_id} → {direction} = {target} (target room doesn't exist)")
                continue
            reverse_map = {"N": "S", "S": "N", "E": "W", "W": "E", "U": "D", "D": "U"}
            reverse = reverse_map.get(direction)
            if reverse:
                reverse_exit = rooms[target].get("exits", {}).get(reverse)
                if reverse_exit != room_id:
                    errors.append(f"Room {room_id} ↔ {direction.upper()}: Room {room_id}→{direction.upper()}={target}, but Room {target}→{reverse}={reverse_exit} (expected {room_id})")
    
    return len(rooms), errors

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    print("Testing bidirectional exits on KIDNAPPED! floors\n")
    results = {}
    for floor in range(9, 0, -1):
        count, result = test_floor(floor)
        if count is None:
            print(f"⚠️  Floor {floor}: {result}")
            results[floor] = ("skip", result)
        elif result:
            print(f"❌ Floor {floor}: {len(result)} error(s)")
            for e in result[:5]:
                print(f"   {e}")
            if len(result) > 5:
                print(f"   ... and {len(result)-5} more")
            results[floor] = ("fail", result)
        else:
            print(f"✅ Floor {floor}: all exits bidirectional ({count} rooms)")
            results[floor] = ("pass", count)
    
    print(f"\n{'='*50}")
    passed = sum(1 for v in results.values() if v[0] == "pass")
    skipped = sum(1 for v in results.values() if v[0] == "skip")
    print(f"Result: {passed} passed, {len(results)-passed-skipped} failed, {skipped} skipped")
