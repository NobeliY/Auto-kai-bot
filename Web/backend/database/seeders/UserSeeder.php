<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class UserSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run(): void
    {
        User::factory(10)->create();
        User::factory(1)->create([
            'id' => 1,
            'initials' => fake()->firstName() . ' ' . fake()->lastName(),
            'email' => fake()->email(),
            'phoneNumber' => fake()->phoneNumber(),
            'group' => '24' . rand(100, 410),
            'stateNumber' => 'A' . rand(100,999) . 'AA|'. rand(1,999),
            'access' => 'S',
        ]);
    }
}
