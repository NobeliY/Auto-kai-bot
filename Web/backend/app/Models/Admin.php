<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;

class Admin extends Model
{
    use HasFactory;

    protected $table = 'admins';

    protected $fillable = [
        'id',
        'login',
        'password',
        'email',
    ];

//    public function user(): HasOne
//    {
//        return $this->hasOne(User::class, 'user', 'id');
//    }
}
