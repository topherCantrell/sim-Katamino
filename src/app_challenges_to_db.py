import challenges
import solutions_db

# Make sure all the game combinations in the challenges are marked as such
# in the solution database. Many of the same combinations appear in multiple
# challenges (a single combination can map to many challenges).


def main():
    for challenge in challenges.CHALLENGES:
        for line in challenge['lines']:
            i = line.index('-')
            name = line[0:i]
            j = line.index(':')
            start_pos = int(line[i + 1:j])
            pies = line[j + 1:]

            for pos in range(start_pos, len(pies)):
                comb = pies[0:pos]
                #print(comb, challenge['title'] + ':' + name)
                solutions_db.add_challenge(
                    comb, challenge['title'] + ':' + name)


main()
