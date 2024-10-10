class Program
{
    static void Main(string[] args)
    {
        IMonster dragon = new Dragon();
        IMonster zombie = new Zombie();

        Console.WriteLine("=== Dragão vs Zumbi ===\n");

        // Combate até que um dos monstros morra
        while (dragon.Life() > 0 && zombie.Life() > 0)
        {
            // Dragão ataca o zumbi
            int dragonDamage = dragon.Attack();
            int zombieDefense = zombie.Defend();
            int damageTakenByZombie = Math.Max(dragonDamage - zombieDefense, 0);
            Console.WriteLine($"O Zumbi recebeu {damageTakenByZombie} de dano após a defesa.");
            zombie.TakeDamage(damageTakenByZombie);

            if (zombie.Life() <= 0)
            {
                Console.WriteLine("O Zumbi foi derrotado! O Dragão vence!");
                break;
            }

            // Zumbi contra-ataca com super ataque
            int zombieSuperDamage = zombie.SuperAttack();
            int dragonDefense = dragon.Defend();
            int damageTakenByDragon = Math.Max(zombieSuperDamage - dragonDefense, 0);
            Console.WriteLine($"O Dragão recebeu {damageTakenByDragon} de dano após a defesa.");
            dragon.TakeDamage(damageTakenByDragon);

            if (dragon.Life() <= 0)
            {
                Console.WriteLine("O Dragão foi derrotado! O Zumbi vence!");
                break;
            }
        }
    }
}
